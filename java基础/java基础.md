## 1.对象

### 1.2 对象在内存中的分配

​    对象分为三部分

​     1.对象头 2.对象数据 3.对齐填充 padding

#### 1.2.1 对象头数据

##### 1.2.1.1 Mark Word 

  对象运行时的数据 例如:  hashCode  thread id  Gc 年龄  lock 信息

对象需要存储的运行时数据很多，其实已经超出了32、64位Bitmap结构所能记录的最大限度，但对象头里
的信息是与对象自身定义的数据无关的额外存储成本，考虑到虚拟机的空间效率，Mark Word被设计成一个有着动态定义的数据结构，以便在
极小的空间内存储尽量多的数据，根据对象的状态复用自己的存储空间。例如在32位的HotSpot虚拟机中，如对象未被同步锁锁定的状态
下，Mark Word的32个比特存储空间中的25个比特用于存储对象哈希码，4个比特用于存储对象分代年龄，2个比特用于存储锁标志位，1个
比特固定为0，在其他状态（轻量级锁定、重量级锁定、GC标记、可偏向）

根据锁状态不同存储信息不同  数据取自hotspot源码 

```c++
//
//  32 bits:
//  --------
//             hash:25 ------------>| age:4    biased_lock:1 lock:2 (normal object)
//             JavaThread*:23 epoch:2 age:4    biased_lock:1 lock:2 (biased object)
//             size:32 ------------------------------------------>| (CMS free block)
//             PromotedObject*:29 ---------->| promo_bits:3 ----->| (CMS promoted object)
//
//  64 bits:
//  --------
//  unused:25 hash:31 -->| unused:1   age:4    biased_lock:1 lock:2 (normal object)
//  JavaThread*:54 epoch:2 unused:1   age:4    biased_lock:1 lock:2 (biased object)
//  PromotedObject*:61 --------------------->| promo_bits:3 ----->| (CMS promoted object)
//  size:64 ----------------------------------------------------->| (CMS free block)
//
//  unused:25 hash:31 -->| cms_free:1 age:4    biased_lock:1 lock:2 (COOPs && normal object)
//  JavaThread*:54 epoch:2 cms_free:1 age:4    biased_lock:1 lock:2 (COOPs && biased object)
//  narrowOop:32 unused:24 cms_free:1 unused:4 promo_bits:3 ----->| (COOPs && CMS promoted object)
//  unused:21 size:35 -->| cms_free:1 unused:7 ------------------>| (COOPs && CMS free block)
//
//  - hash contains the identity hash value: largest value is
//    31 bits, see os::random().  Also, 64-bit vm's require
//    a hash value no bigger than 32 bits because they will not
//    properly generate a mask larger than that: see library_call.cpp
//    and c1_CodePatterns_sparc.cpp.

//  - the biased lock pattern is used to bias a lock toward a given
//    thread. When this pattern is set in the low three bits, the lock
//    is either biased toward a given thread or "anonymously" biased,
//    indicating that it is possible for it to be biased. When the
//    lock is biased toward a given thread, locking and unlocking can
//    be performed by that thread without using atomic operations.
//    When a lock's bias is revoked, it reverts back to the normal
//    locking scheme described below.

//    Note that we are overloading the meaning of the "unlocked" state
//    of the header. Because we steal a bit from the age we can
//    guarantee that the bias pattern will never be seen for a truly
//    unlocked object.

//    Note also that the biased state contains the age bits normally
//    contained in the object header. Large increases in scavenge
//    times were seen when these bits were absent and an arbitrary age
//    assigned to all biased objects, because they tended to consume a
//    significant fraction of the eden semispaces and were not
//    promoted promptly, causing an increase in the amount of copying
//    performed. The runtime system aligns all JavaThread* pointers to
//    a very large value (currently 128 bytes (32bVM) or 256 bytes (64bVM))
//    to make room for the age bits & the epoch bits (used in support of
//    biased locking), and for the CMS "freeness" bit in the 64bVM (+COOPs).
//
//    [JavaThread* | epoch | age | 1 | 01]       lock is biased toward given thread
//    [0           | epoch | age | 1 | 01]       lock is anonymously biased
//
//  - the two lock bits are used to describe three states: locked/unlocked and monitor.
//
//    [ptr             | 00]  locked             ptr points to real header on stack
//    [header      | 0 | 01]  unlocked           regular object header
//    [ptr             | 10]  monitor            inflated lock (header is wapped out)
//    [ptr             | 11]  marked             used by markSweep to mark an object
//                                               not valid at any other time
//
//    We assume that stack/thread pointers have the lowest two bits cleared.

class BasicLock;
class ObjectMonitor;
class JavaThread;

class markOopDesc: public oopDesc {
 private:
  // Conversion
  uintptr_t value() const { return (uintptr_t) this; }

 public:
  // Constants
  enum { age_bits                 = 4,
         lock_bits                = 2,
         biased_lock_bits         = 1,
         max_hash_bits            = BitsPerWord - age_bits - lock_bits - biased_lock_bits,
         hash_bits                = max_hash_bits > 31 ? 31 : max_hash_bits,
         cms_bits                 = LP64_ONLY(1) NOT_LP64(0),
         epoch_bits               = 2
  };

  // The biased locking code currently requires that the age bits be
  // contiguous to the lock bits.
  enum { lock_shift               = 0,
         biased_lock_shift        = lock_bits,
         age_shift                = lock_bits + biased_lock_bits,
         cms_shift                = age_shift + age_bits,
         hash_shift               = cms_shift + cms_bits,
         epoch_shift              = hash_shift
  };

```

​     ---  无锁 
​     ---  偏向锁
​     ---  轻量锁
​     ---  重量锁 
​     ---  GC

| 锁状态 | 25 bit          | 31bit       | 1bit               | 4bit     | 1bit         | 2bit     |
| ------ | --------------- | ----------- | ------------------ | -------- | ------------ | -------- |
| ------ |                 |             | cms_free           | 分代年龄 | 是否为偏向锁 | 锁标志位 |
| 无锁   | unused          | hashCode    | 1                  |          | 0            | 01       |
| 偏向锁 | ThreadId(54bit) | epoch(2bit) | 1                  |          | 1            | 01       |
| 轻量锁 |                 |             | 指向锁记录的指针   |          |              | 00       |
| 重量锁 |                 |             | 指向重量级锁的指针 |          | 0            | 10       |
| GC     |                 |             | 空                 |          |              | 11       |

![image-20200602102045060](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20200602102045060.png)

##### 1.2.1.2   对象类型指针

即对象指向它的类型元数据的指针，Java虚拟机通过这个指针来确定该对象是哪个类的实例。并不是所
有的虚拟机实现都必须在对象数据上保留类型指针，换句话说，查找对
象的元数据信息并不一定要经过对象本身

#### 1.2 .2对象实例数据

实例数据部分是对象真正存储的有效信息，即我们在程序代码里面所定义的各种类型的字段内容，无论是从父类继承下来的，还是
在子类中定义的字段都必须记录起来。这部分的存储顺序会受到虚拟机分配策略参数（-XX：FieldsAllocationStyle参数）和字段在Java源码中
定义顺序的影响。HotSpot虚拟机默认的分配顺序为longs/doubles、ints、shorts/chars、bytes/booleans、oops（Ordinary Object Pointers，
OOPs），从以上默认的分配策略中可以看到，相同宽度的字段总是被分配到一起存放，在满足这个前提条件的情况下，在父类中定义的变量
会出现在子类之前。如果HotSpot虚拟机的+XX：CompactFields参数值为true（默认就为true），那子类之中较窄的变量也允许插入父类变量的
空隙之中，以节省出一点点空间.(摘自 深入理解java虚拟机(第三版) 周志明 )

#### 1.2.3对齐填充 

对象的第三部分是对齐填充，这并不是必然存在的，也没有特别的含义，它仅仅起着占位符的作用。由于HotSpot虚拟机的自动内存管理
系统要求对象起始地址必须是8字节的整数倍，换句话说就是任何对象的大小都必须是8字节的整数倍。对象头部分已经被精心设计成正好是8
字节的倍数（1倍或者2倍），因此，如果对象实例数据部分没有对齐的话，就需要通过对齐填充来补全。

### 1.3 对象的访问  

对象的访问有两种方式 一种是句柄访问,一种是直接访问.

####  1.3.1 句柄访问

 由java栈 reference 指向句柄  (java 堆中单独的一个区域) , 句柄中包含了对象
实例数据与类型数据各自具体的地址信息. 

优点是:  使用句柄来访问的最大好处就是reference中存储的是稳定句柄地址，在对象被移动（垃圾收集时移动对
象是非常普遍的行为）时只会改变句柄中的实例数据指针，而reference本身不需要被修改。

结构如下图所示 :

![image-20200602144315810](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20200602144315810.png)

#### 1.3.2 直接访问

由reference 引用直接访问对象  Java堆中对象的内存布局就必须考虑如何放置访问类型数据的相关信息，reference中存储的直接就是对象地
址，如果只是访问对象本身的话，就不需要多一次间接访问的开销.Hotspot 主要就是使用这种方式 

结构如下图所示:

​                               ![image-20200602144548594](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20200602144548594.png)  





## 2. 垃圾回收

​      垃圾回收 三个问题 ?

1. 那些内存需要回收   2. 何时回收  3.如何回收

### 2.1 如何确定对象已死

   java 堆中存放在对象,在回收之前第一件事就是要确定那些对象已死,那些对象活着。

#### 2.1.1 引用计数法

在对象中添加一个引用计数器，当有一个引用指向对象时，就引用计数器就加一。 当一个引用失效，引用计数器就减一，当引用失效
时，计数器值就减一，任何时刻计数器为零的对象就是不可能再被使用的。

虽然效率很高但是会有一个问题：

 循环引用  例如 A引用B  B引用C C引用A 这会导致三个对象都引用计数 都不为0 ,永远无法被回收。

#### 2.1.2 可达性分析算法

这个算法的基本思路就是通过一系列称为“GC Roots”的根对象作为起始节点集，从这些节点开始，根据引用关系向下搜索，搜索过程所走过的路径称为“引用链”（ReferenceChain），如果某个对象到GC Roots间没有任何引用链相连，或者用图论的话来说就是从GC Roots到这个对象不可达时，则证明此对象是不可能再被使用的。

JAVA 中GC ROOTS 包含以下几类：

·在虚拟机栈（栈帧中的本地变量表）中引用的对象，譬如各个线程被调用的方法堆栈中使用到的参数、局部变量、临时变量等。

·在方法区中类静态属性引用的对象，譬如Java类的引用类型静态变量。

·在方法区中常量引用的对象，譬如字符串常量池（String Table）里的引用。

·在本地方法栈中JNI（即通常所说的Native方法）引用的对象。

·Java虚拟机内部的引用，如基本数据类型对应的Class对象，一些常驻的异常对象（比如NullPointExcepiton、OutOfMemoryError）等，还有系统类加载器。

·所有被同步锁（synchronized关键字）持有的对象。

·反映Java虚拟机内部情况的JMXBean、JVMTI中注册的回调、本地代码缓存等。

### 2.2  垃圾收集

#### 2.2.1 分代收集

#### 2.2.2 标记-清除

算法分为“标记”和“清除”两个阶段：首先标记出所有需要回收的对象，在标记完成后，统一回收掉所有被标记的对象，也可以反过来，
标记存活的对象，统一回收所有未被标记的对象。

优点 简单.

缺点 : 内存碎片,提前gc

![image-20200602161727021](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20200602161727021.png)

#### 2.2.3 标记-复制

标记-复制算法常被简称为复制算法。为了解决标记-清除算法面对大量可回收对象时执行效率低的问题，它将可用内存按容量划分为大小相等的两块，每次只使用其中的一块。当这一块的内存用完了，就将还存活着的对象复制到另外一块上面，然后再把已使用过的内存空间一次清理掉。多用于新生代   

Eden : Survivor    8:1

优点: 简单 运行高效

缺点 :如果内存中多数对象都是存活的，这种算法将会产生大量的内存间复制的开销. 浪费内存. 

![image-20200602162216622](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20200602162216622.png)

#### 2.2.4 标记-整理

其中的标记过程仍然与“标记-清除”算法一样，但后续步骤不是直接对可回收对象进行清理，而是让所有存活的对象都向内存空间一端移动，然后直接清理掉边
界以外的内存.标记-清除算法与标记-整理算法的本质差异在于前者是一种非移动式的回收算法，而后者是移动式的。多用于老年代

优点:解决了空间碎片

缺点:大量移动对象,会阻塞用户线程 

![image-20200602162949855](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20200602162949855.png)

### 2.3 对象分配

大多数情况下，对象在新生代Eden区中分配。当Eden区没有足够空间进行分配时，虚拟机将发起一次Minor GC



## 3.类文件结构

### 3.1 魔数

每个class文件的前四个字节被称为魔数,它唯一确定这个文件是否是可以被虚拟机接受的Class文件.紧接着魔数的4个字节存储的是Class文件的版本号：第5和第6个字节是次版本号（Minor Version），第7和第8个字节是主版本号（MajorVersion）。JVM 只能执行之前的的 class文件不能执行之后的文件。

### 3.2 常量池

紧接着主、次版本号之后的是常量池入口，常量池可以比喻为Class文件里的资源仓库，它是Class文件结构中与其他项目关联最多的数据，
通常也是占用Class文件空间最大的数据项目之一，另外，它还是在Class文件中第一个出现的表类型数据项目。

## 4.类加载机制

### 4.1 类加载时机

一个class文件的生命周期 有 加载（loading） 验证（verification） 准备（preparation） 解析（Resolution） 初始化（Initialization） 使用（using） 卸载（Unloading） 七个阶段，其中 验证，准备,解析阶段被称为连接。 如下图示

![image-20200603101313986](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20200603101313986.png)

### 4.2 类加载过程

#### 4.2.1 加载 

加载jvm 需要做三件事:

1) 通过一个类的全限定名获取定义此类的一个二进制字节流。

2）将这个字节流所代表的静态存储结构转化为方法区的运行时数据结构。

3）在内存中生成代表这个类的 java.lang.class 对象,作为方法区这个类各类数据访问入口.

#### 4.2.2 验证

验证是连接阶段的第一步，这一阶段的目的是确保Class文件的字节流中包含的信息符合《Java虚拟机规范》的全部约束要求，保证这些信
息被当作代码运行后不会危害虚拟机自身的安全。验证分为四种: 文件格式验证, 元数据认证,,字节码验证,符号引用认证

#### 4.2.3  准备

#### 4.2.4 解析

#### 4.2.5 初始化

### 4.3 类加载器

启动类加载器

拓展类加载器

应用程序类加载器

## 5.多线程






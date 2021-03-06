## 1.架构演进

### 1.1 单体系统时代：应用最广泛的架构风格

大型单体系统单体架构是绝大部分软件开发者都学习和实践过的一种软件架构，很多介绍微服务的图书和技术资料中，也常常会把这种架构形式的应用称作“巨石系统”（Monolithic Application）。

####  单体架构的优点

对于小型系统，也就是用单台机器就足以支撑其良好运行的系统来说，这样的单体不仅易于开发、易于测试、易于部署，而且因为各个功能、模块、方法的调用过程，都是在进程内调用的，不会发生进程间通讯，所以程序的运行效率也要比分布式系统更高。

#### 单体架构的缺陷

**1.复杂性高**
 整个项目包含的模块非常多，模块的边界模糊，依赖关系不清晰，代码质量参差不齐,整个项目非常复杂。每次修改代码都心惊胆战，甚至添加一个简单的功能，或者修改一个BUG都会造成隐含的缺陷。

**2.技术债务逐渐上升**
 随着时间推移、需求变更和人员更迭，会逐渐形成应用程序的技术债务，并且越积越多。已使用的系统设计或代码难以修改，因为应用程序的其他模块可能会以意料之外的方式使用它。

**3.部署速度逐渐变慢**
 随着代码的增加，构建和部署的时间也会增加。**而在单体应用中，每次功能的变更或缺陷的修复都会导致我们需要重新部署整个应用。**全量部署的方式耗时长、影响范围大、风险高，这使得单体应用项目上线部署的频率较低，从而又导致两次发布之间会有大量功能变更和缺陷修复，出错概率较高。

**4.扩展能力受限，无法按需伸缩**
 单体应用只能作为一个整体进行扩展，无法结合业务模块的特点进行伸缩。

**5.阻碍技术创新**
 单体应用往往使用统一的技术平台或方案解决所有问题，团队的每个成员都必须使用相同的开发语言和架构，想要引入新的框架或技术平台非常困难。

由于单体架构的缺陷日益明显，所以越来越多的公司采用**微服务**架构范式解决上面提到的单体架构中的问题。

### 1.2 SOA架构 面向服务架构（Service-Oriented Architecture）

 SOA 的概念最早是由 Gartner 公司在 1994 年提出的。当时的 SOA 还不具备发展的条件，直到 2006 年情况才有所变化，IBM、Oracle、SAP 等公司，共同成立了 OSOA 联盟（Open Service Oriented Architecture），来联合制定和推进 SOA 相关行业标准。到 2007 年，在结构化资讯标准促进组织（Organization for the Advancement of Structured Information Standards，OASIS）的倡议与支持下，OSOA 就由一个软件厂商组成的松散联盟，转变为了一个制定行业标准的国际组织。它联合 OASIS 共同新成立了Open CSA组织（Open Composite Services Architecture），也就是 SOA 的“官方管理机构”。

SOA 不能说是一种软件架构，是一种设计方法，包含多个服务，服务之间相互依赖，最终提供一系列功能，一个服务 通常以独立的形式存在,各系统间通过网络调用。

EBS

![image-20210127160848583](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20210127160848583.png)

###  1.3 微服务架构 

微服务架构风格，就像是把一个单独的应用程序开发为一套小服务，每个小服务运行在自己的进程中，并使用轻量级机制通信，通常是 HTTP API。这些服务围绕业务能力来构建，并通过完全自动化部署机制来独立部署。这些服务使用不同的编程语言书写，以及不同数据存储技术，并保持最低限度的集中式管理。

![image-20210125143003650](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20210125143003650.png)

微服务的特点：

#### 服务间调用

在单体应用中，组件间直接通过函数调用的方式进行交互协作。而在微服务架构中，由于服务不在一个进程中，组件间的通信模式发生了改变，若仅仅将原本在进程内的方法调用改成RPC 方式的调用，会导致微服务之间产生烦琐的通信，使得系统表现更为糟糕，所以，我们需要更粗粒度的通信协议。
在微服务架构中，通常会使用以下两种服务调用方式：
		· 第一种，使用HTTP 的RESTful API 或轻量级的消息发送协议，实现信息传递与服
务调用的触发。
		· 第二种，通过在轻量级消息总线上传递消息，类似RabbitMQ 等一些提供可靠异步
交换的中间件。
		在极度强调性能的情况下，有些团队会使用二进制的消息发送协议，例如protobuf。即使是这样，这些系统仍然会呈现出“智能端点和哑管道”的特点，这
是为了在易读性与高效性之间取得平衡。当然大多数Web 应用或企业系统并不需要在这两者间做出选择，能够获得易读性已经是一个极大的胜利了。
   																																											—Martin Fowler

#### 去中心化治理

​		当我们采用集中化的架构治理方案时，通常在技术平台上都会制定统一的标准， 但是每一种技术平台都有其短板，这会导致在碰到短板时，不得不花费大力气去解决， 并且可能因为其底层原因解决得不是很好，最终成为系统的瓶颈。在实施微服务架构时，通过采用轻量级的契约定义接口，使得我们对于服务本身的具体技术平台不再那么敏感，这样整个微服务架构系统中的各个组件就能针对其不同的业务特点选择不同的技术平台，终于不会出现杀鸡用牛刀或是杀牛用指甲钳的尴尬处境了。

#### 去中心化管理数据

​		我们在实施微服务架构时，都希望让每一个服务来管理其自有的数据库，这就是数据管理的去中心化。在去中心化过程中，我们除了将原数据库中的存储内容拆分到新的同平台的其他数据库实例中之外（ 如把原本存储在MySQL 中的表拆分后， 存储到多个不同的MySQL 实例中），
也可以将一些具有特殊结构或业务特性的数据存储到一些其他技术的数据库实例中（ 如把日志信息存储到MongoDB 中或把用户登录信息存储到Redis 中） 。虽然数据管理的去中心化可以让数据管理更加细致化， 通过采用更合适的技术可让数据存储和性能达到最优。但是，由千数据存储千不同的数据库实例中后，数据一致性也成为微服务架构中亟待解决的问题之一。分布式事务本身的实现难度就非常大，所以在微服务架构中，我们更强调在各服务之间进行“无事务”的调用，而对于数据一致性，只要求数据在最后的处理状态是一致的即可；若在过程中发现错误，通过补偿机制来进行处理，使得错误数据能够达到最终的一致性。

#### 基础设施自动化

近年来云计算服务与容器化技术的不断成熟，运维基础设施的工作变得越来越容易。但是，当我们实施微服务架构时，数据库、应用程序的个头虽然都变小了，但是因为拆分的原因，数量成倍增长。这使得运维人员需要关注的内容也成倍增长，并且操作性任务也会成倍增长，这些问题若没有得到妥善解决，必将成为运维人员的噩梦。所以，在微服务架构中，务必从一开始就构建起“持续交付“平台来支撑整个实施过
程， 该平台需要两大内容，缺一不可。
		·自动化测试： 每次部署前的强心剂， 尽可能地获得对正在运行的软件的信心。
		·自动化部署： 解放烦琐枯燥的重复操作以及对多环境的配置管理。

#### 容错设计

​		在单体应用中， 一般不存在单个组件故障而其他部件还在运行的情况，通常是一挂全挂。而在微服务架构中，由于服务都运行在独立的进程中，所以存在部分服务出现故障，而其他服务正常运行的情况。比如，当正常运作的服务B 调用到故障服务A 时，因故障服务A 没有返回，线程挂起开始等待，直到超时才能释放，而此时若触发服务B 调用服务A的请求来自服务C, 而服务C 频繁调用服务B 时，由于其依赖服务A, 大量线程被挂起等待，最后导致服务A 也不能正常服务，这时就会出现故障的蔓延。所以，在微服务架构中，快速检测出故障源并尽可能地自动恢复服务是必须被设计和考虑的。通常，我们都希望在每个服务中实现监控和日志记录的组件，比如服务状态、断路器状态、吞吐量、网络延迟等关键数据的仪表盘等。演进式设计通过上面的几点特征，我们已经能够体会到，要实施一个完美的微服务架构，需要考虑的设计与成本并不小，对于没有足够经验的团队来说，甚至要比单体应用付出更多的代价。
​	所以，在很多情况下，架构师都会以演进的方式进行系统的构建。在初期，以单体系统的方式来设计和实施， 一方面系统体量初期并不会很大，构建和维护成本都不高。另一方面，初期的核心业务在后期通常也不会发生巨大的改变。随着系统的发展或者业务的需要，架构师会将一些经常变动或是有一定时间效应的内容进行微服务处理，并逐渐将原来在单体系统中多变的模块逐步拆分出来，而稳定不太变化的模块就形成一个核心微服务存在于整个架构之中。

微服务缺点 

1. 需要更多的资源
2. 更复杂的事务控制
3. 更复杂的运维

下一代架构 ？ServiceMesh



## 2 spring cloud 

Spring Cloud为开发人员提供了工具来快速构建分布式系统中的一些常见模式（例如配置管理，服务发现，断路器，智能路由，微代理，控制总线）。 分布式系统的协调导致了样板式样，并且使用Spring Cloud开发人员可以快速站起来实现这些样板的服务和应用程序。 它们可以在任何分布式环境中很好地工作，包括开发人员自己的笔记本电脑，裸机数据中心以及Cloud Foundry等托管平台，spring cloud 是微服务的落地实现。

它目前由Spring 官方开发维护，基千Spring Boot 开发，提供一套完整的微服务解决方案。包括服务注册与发现、配置中心、全链路监控、API 网关、熔断器等选型中立的开源组件，可以随需扩展和替换组装。

### 版本选择

Spring Boot的版本以数字表示。例如：Spring Boot 2.2.5.RELEASE --> 主版本.次版本.增量版本（Bug修复）
版本号介绍：

- Alpha：不建议使用，主要是以实现软件功能为主，通常只在软件开发者内部交流，Bug较多；
- Beta：该版本相对于α版已有了很大的改进，消除了严重的错误，但还是存在着一些缺陷，需要经过多次测试来进一步消除；
- GA：General Availability，正式版本，官方推荐使用此版本，在国外都是用GA来说明release版本；
- M：又叫里程碑版本，表示该版本较之前版本有功能上的重大更新；
- PRE(不建议使用)：预览版，内部测试版，主要是给开发人员和测试人员测试和找BUG用的；
- Release：最终版本，Release不会以单词形式出现在软件封面上，取而代之的是符号(R)；
- RC：该版本已经相当成熟了，基本上不存在导致错误的BUG，与即将发行的正式版相差无几；
- SNAPSHOT：快照版，可以稳定使用，且仍在继续改进版本。

SpringCloud 版本介绍

官网链接：https://spring.io/projects/spring-cloud#learn

Spring Cloud是一个项目总括，里面包含了很多的子项目，避免子项目之间的混淆，因此命名方式采用英文名字的方式来命名，Spring Cloud的名字以Release Trains的形式，采用伦敦地铁站，以A-Z字母顺序表发布,  2020年 开始 使用日历版本命名   https://calver.org/ 

- SR.X 修正版，服务版本，当项目发布积累到一定程度，需要修复该版本中的某个错误后以此来命名，X表示数字。

版本对应关系 

https://start.spring.io/actuator/info

### spring cloud 组件

 

![image-20210125181719941](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20210125181719941.png)

##### Spring Cloud 与服务治理中间件
​		服务治理中间件包含服务注册与发现、服务路由、负载均衡、自我保护、丰富的治理管理机制等功能。其中服务路由包含服务上下线、在线测试、机房就近选择、AIB 测试、灰度发布等。负载均衡支持根据目标状态和目标权重进行负载均衡。自我保护包括服务降级、优雅降级和流量控制。Spring Cloud 作为一个服务治理中间件，它的服务治理体系做了高度的抽象，目前支持使用Eureka 、Zookeeper 、Consul ，nacos作为注册中心，并且预留了扩展接口，而且由于选型是中立
的，所以支持无缝替换。在Spring Cloud 中可以通过Hystrix 进行熔断自我保护Fallback, 通过Ribbon 进行负载均衡。

##### CAP理论

CAP理论是分布式架构中重要理论

> 一致性(Consistency) (所有节点在同一时间具有相同的数据) 可用性(Availability) (保证每个请求不管成功或者失败都有响应) 分隔容忍(Partition tolerance) (系统中任意信息的丢失或失败不会影响系统的继续运作)

各个注册中心对比 

![image-20210127143249531](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20210127143249531.png)

###### Eureka



Eureka采用了CS的设计架构，Eureka Server作为服务注册功能的服务器，它是服务注册中心。而系统中的其他微服务，使用Eureka的客户端连接到Eureka Server并维持心跳连接。这样系统的维护人员就可以通过Eureka Server来监控系统中各个微服务是否正常运行。

在服务注册与发现中，有一个注册中心。当服务器启动的时候，会把当前自己服务器的信息比如服务地址通讯地址等**以别名方式**注册到注册中心上。另一方(消费者|服务提供者)，以该别名的方式去注册中心上**获取到实际的服务通讯地址**,然后再实现本地RPC调用RPC远程调用。

**框架核心设计思想**:在于注册中心，因为使用注册中心管理每个服务与服务之间的一个依赖关系(**服务治理概念**)。在任何rpc远程框架中，都会有一个注册中心(存放服务地址相关信息(接口地址))



![image-20210127140750585](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20210127140750585.png)

###### consul：

  和 eureka 对比  https://www.consul.io/docs/intro/vs/eureka

Consul 是 HashiCorp 公司推出的开源工具，用于实现分布式系统的服务发现与配置。Consul 使用 Go 语言编写，因此具有天然可移植性（支持Linux、windows和Mac OS X）。

Consul 内置了服务注册与发现框架、分布一致性协议实现、健康检查、Key/Value 存储、多数据中心方案，不再需要依赖其他工具（比如 ZooKeeper 等），使用起来也较为简单。

Consul 遵循CAP原理中的CP原则，保证了强一致性和分区容错性，且使用的是Raft算法，比zookeeper使用的Paxos算法更加简单。虽然保证了强一致性，但是可用性就相应下降了，例如服务注册的时间会稍长一些，因为 Consul 的 raft 协议要求必须过半数的节点都写入成功才认为注册成功 ；在leader挂掉了之后，重新选举出leader之前会导致Consul 服务不可用。

与Zookeeper和etcd不一样，Consul内嵌实现了服务发现系统，所以这样就不需要构建自己的系统或使用第三方系统。这一发现系统除了上述提到的特性之外，还包括节点健康检查和运行在其上的服务。

Consul强一致性(C)带来的是：

1. 服务注册相比Eureka会稍慢一些。因为Consul的raft协议要求必须过半数的节点都写入成功才认为注册成功
2. Leader挂掉时，重新选举期间整个consul不可用。保证了强一致性但牺牲了可用性。

###### zookeeper：

ZooKeeper是由雅虎开发并开源的分布式协调服务。ZooKeeper提供了统一命名服务、配置管理、分布式锁等基础服务，基于这些基础服务，我们可以实现集群管理、软负载、发布/订阅、命名服务等功能。最重要的功能 是分布式协调。

　　ZooKeeper维护着一种像文件系统的一种结构树。如下图：

![image-20210128142833869](C:\Users\dongw\AppData\Roaming\Typora\typora-user-images\image-20210128142833869.png)

图中每个都是一个节点(ZNode)，节点可以包含数据，也可以没有，每个节点都有自己的权限。

​		服务发现就是将服务提供者信息主动上报到服务注册中心进行服务注册，如将其提供的服务和对应的IP和端口注册到ZooKeeper中，服务调用者启动的时候，将ZooKeeper注册中心信息下拉倒服务调用者本机缓存，到需要用到到某个服务时，通过某种算法，去选择其中一个IP+端口，然后调用。

###### nac0s:

Nacos是阿里开源的，Nacos 支持基于 DNS 和基于 RPC 的服务发现。在Spring Cloud中使用Nacos，只需要先下载 Nacos 并启动 Nacos server，Nacos只需要简单的配置就可以完成服务的注册发现。

Nacos除了服务的注册发现之外，还支持动态配置服务。动态配置服务可以让您以中心化、外部化和动态化的方式管理所有环境的应用配置和服务配置。动态配置消除了配置变更时重新部署应用和服务的需要，让配置管理变得更加高效和敏捷。配置中心化管理让实现无状态服务变得更简单，让服务按需弹性扩展变得更容易。

https://nacos.io/zh-cn/docs/what-is-nacos.html

#####  Spring Cloud 与配置中心中间件
在单体应用中，我们一般的做法是把属性配置和代码硬编码放在一起，这没有什么问题。但是在分布式系统中，由于存在多个服务实例，需要分别管理每个具体服务工程中的配置，上线需要准备Check List 并逐个检查每个上线的服务是否正确。在系统上线之后一旦修改某个配置，就需要重启服务。这样开发管理相当麻烦。因此我们需要把分布式系统中的配置信息抽取出来统一管理，这个管理的中间件称为配置中心。配置中心应该具备的功能，分别是支持各种复杂的配置场景，与公司的运维体系和权限管理体系集成，各种配置兼容支持，

Spring Cloud Config 是Spring Cloud 生态圈中的配置中心中间件，它把应用原本放在本地文件中的配置抽取出来放在中心服务器，从而能够提供更好的管理、发布能力。Spring CloudConfig 基于应用、环境、版本三个维度管理，配置存储支持Git 和其他扩展存储，且无缝支持Spring 里Environment 和PropertySource 的接口。但是Spring Cloud Config 的缺点是没有可视化的管控平台，因此会用其他的配置中心中间件取代它管理配置，例如 ，nocas。


##### Spring Cloud 与网关中间件

1．网关中间件概述
API Gateway (APIGW/API 网关），顾名思义，是出现在系统边界上一个面向API 的、串行集中式的强管控服务，这里的边界是企业IT 系统的边界，可以理解为企业级应用防火墙，主要起到隔离外部访问与内部系统的作用。在微服务概念流行之前， API 网关就已经诞生了，例如银行、证券等领域常见的前置系统，它的设计与出现主要是为了解决访问认证、报文转换、访问统计等问题。网关在微服务架构中所处的位置，随着微服务架构概念的提出， API 网关成为微服务架构的一个标配组件。作为一个网关中间件，至少具备如下四大功能。
		(1) 统一接入功能为各种无线应用提供统一的接入服务，提供一个高性能、高并发、高可靠的网关服务。不
仅如此，还要支持负载均衡、容灾切换和异地多活。

​		(2) 协议适配功能网关对外的请求协议一般是HTTP 或HTTP2 协议，而后端提供访问的服务协议要么是REST 协议要么是RPC 协议。网关需要根据请求进来的协议进行协议适配，然后协议转发调用不同协议提供的服务。比如网关对外暴露是HTTP 协议的请求，而网关后端服务可能是Dubbo 提供的RPC 服务，可能是Spring Cloud 提供的REST 服务，也可能是其他PHP 编写的服务。当一个HTTP 请求经过网关时，通过一系列不同功能的Filter 处理完毕之后，此时就需要进行协议适配，判断应该协议转发调用RPC 服务，调用REST 服务，还是调用PHP 提供的服务。

​		(3) 流量管控功能
​		网关作为所有请求流量的人口，当请求流量瞬间剧增，比如天猫双11 、双12 或者其他大促活动，流量会迅速剧增，此时需要进行流量管控、流量调拨。当后端服务出现异常，服务不可用时，需要网关进行熔断和服务降级。在异地多活场景中需要根据请求流量进行分片，路由到不同的机房。
​		(4) 安全防护功能
​		网关需要对所有请求进行安全防护过滤，保护后端服务。通过与安全风控部门合作，对IP黑名单和URL 黑名单封禁控制，做风控防刷，防恶意攻击等。

2. Spring Cloud 第一代网关Zuul

  		Spring Cloud 生态圈的第一代网关是在Netflix 公司开源的网关组件Zuul 之上，它基于Spring Boot 注解，采用Starter 的方式进行二次封装，可以做到开箱即用。目前Zuul 融合了Spring Cloud 提供的服务治理体系，根据配置的路由规则或者默认的路由规则进行路由转发和负载均衡。它可以与Spring Cloud 生态系统内其他组件集成使用，例如：集成Hystrix 可以在网关层面实现降级的功能；集成Ribbon 可以使得整个架构具备弹性伸缩能力；集成Archaius可以进行配置管理等。但是Spring Cloud Zuul 如果需要做一些灰度、降级、标签路由、限流、WAF 封禁，则需要自定义Filter 做一些定制化实现。

3. Spring Cloud 第二代网关Gateway
    Spring Cloud Zuul 处理每个请求的方式是分别对每个请求分配一个线程来处理。根据参考数据统计，目前Zuul 最多能达到1000 至2000 QPS 。在高并发的场景下，不推荐使用Zuul 作为网关。因此出现了Spring Cloud 的第二代网关，即Spring Cloud Gateway 。Spring Cloud Gateway 是Spring 官方基于Spring 5.0 、Spring Boot 2.0 和Project Reactor 等技术开发的网关，旨在为微服务架构提供一种简单、有效、统一的API 路由管理方式。SpringCloud Gateway 底层基千Netty 实现(Netty 的线程模型是多线程reactor 模型，使用boss 线程和worker 线程接收并异步处理请求，具有很强大的高并发处理能力），因此Spring Cloud
    Gateway 出现的目的就是替代Netflix Zuul。其不仅提供统一的路由方式，并且基千Filter 链的方式提供了网关基本的功能，例如，安全、监控／埋点、限流等。

  ##### Spring Cloud 与全链路监控中间件

  众所周知，中大型互联网公司的后台业务系统由众多的分布式应用组成。一个通过浏览器或移动客户端的前端请求到后端服务应用，会经过很多应用系统，并且留下足迹和相关日志信息。但这些分散在每个业务应用主机下的日志信息不利千问题排查和定位问题发生的根本原
  因。此时就需要利用全链路监控中间件收集、汇总并分析日志信息，进行可视化展示和监控告
  警。全链路监控中间件应该提供的主要功能包括：
  □ 定位慢调用：包括慢Web 服务（包括Restful Web 服务）、慢REST 或RPC 服务、慢SQL。
  □ 定位各种错误：包括4XX 、5X X 、Service Error 。
  □ 定位各种异常：包括Error Exception 、Fatal Exception 。
  □ 展现依赖和拓扑：域拓扑、服务拓扑、trace 拓扑。
  □ Trace 调用链：将端到端的调用，以及附加在这次调用的上下文信息，异常日志信息，
  每一个调用点的耗时都呈现给用户进行展示。
  □ 应用告警：根据运维设定的告警规则，扫描指标数据，如违反告警规则，则将告警信
  息上报到中央告警平台。
  全链路监控中间件相关产品发展至今百花齐放，如京东Hydra, 阿里Eagleye, 这两个中间件都吸收了Dapper/Zipkin 的设计思路，但是目前都未开源。近年，社区又发展出很多调用链监控产品，如国内开源爱好者吴晟（原OneAPM 工程师，目前在华为）开源并提交到Apache孵化器的产品Skywalking, 它同时吸收了Zipkin/Pinpoint/CAT 的设计思路，支持非侵入式埋点。如果使用Java 技术栈，希望采用非侵入式的监控，推荐使用Pinpoint 或者Skywalking 。



  
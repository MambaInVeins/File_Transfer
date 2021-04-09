LMDB的全称是Lightning Memory-Mapped Database，它的文件结构简单，包含一个数据文件和一个锁文件。

LMDB文件可以同时由多个进程打开，具有极高的数据存取速度，访问简单，不需要运行单独的数据库管理进程，只要在访问数据的代码里引用LMDB库，访问时给文件路径即可。

让系统访问大量小文件的开销很大，而LMDB使用内存映射的方式访问文件，使得文件内寻址的开销非常小，使用指针运算就能实现。数据库单文件还能减少数据集复制/传输过程的开销。

在python中使用lmdb： 使用指令pip install lmdb安装lmdb包。

LightningMemory-MappedDatabase（LMDB）是一个软件库，它以键值存储的形式提供高性能的嵌入式事务数据库。LMDB是用C语言编写的，具有多种编程语言的API绑定。LMDB将任意键/数据对存储为字节数组，具有基于范围的搜索功能，支持单个键的多个数据项，并具有在数据库末尾附加记录的特殊模式（MDB_APPEND），可提供显着的写入性能比其他同类商店增加。LMDB不是关系数据库，它是严格的键值存储等的BerkeleyDB和dbm。

LMDB也可以使用同时在多线程或多处理环境中，有读性能通过设计线性缩放。LMDB数据库一次只能有一个编写器，但与许多类似的键值数据库不同，写事务不会阻止读者，也不会阻止编写器。LMDB也很不寻常，因为同一系统上的多个应用程序可以同时打开并使用相同的LMDB存储，作为扩展性能的手段。此外，LMDB不需要事务日志（从而通过不需要两次写入数据来提高写入性能），因为它通过设计本身维护数据完整性。

LMDB内部使用B+树数据结构。其设计效率和占用空间小，同时具有提供良好写入性能的意外副作用。LMDB有一个类似于BerkeleyDB和dbm的API。LMDB将计算机的内存视为单个地址空间，使用具有写时复制语义的共享内存在多个进程或线程之间共享（历史上称为单级存储）。

​由于大多数以前的现代计算体系结构具有32位内存地址空间限制，这对使用此类技术的任何数据库的大小施加了4GB的硬限制，因此将数据库直接映射到单级存储的技术的有效性严格限制。然而，今天的64位处理器现在主要实现48位地址空间，允许访问47位地址或128TB的数据库大小，使得使用共享内存的数据库在实际应用程序中再次有用。


http://www.lmdb.tech/doc/index.html API官网
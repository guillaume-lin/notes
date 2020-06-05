https://techvidvan.com/tutorials/apache-spark-performance-tuning/
spark 概念
* job  一组并发执行的任务（task）成为作业
* task 工作单元，由每个executor执行，一个task对应一个partition
* stage  一个job由多个stage组成，每个stage包含多个task
* dag 有向无环图
  由节点和边组成，节点可以看成是数据，边看成是对数据的操作。节点可以看成是一个RDD的partition
  
整个spark的运行就是对RDD进行操作

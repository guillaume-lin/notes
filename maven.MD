lifecycle, phase, goal
lifecycle: default,clean,site
phase: validate, compile,test,package,verify,install,deploy
goal:
#基本语法
maven [options] [<goal(s)>] [<phase(s)>]
phase分为:
compile
package

goals有:
# 显示maven archetype
mvn archetype:generate -Dfilter=org.apache.maven.archetypes:
# 编译
mvn compile
#打包
mvn package
#运行
mvn exec:java -Dexec.mainClass="com.hengan.App"  -Dexec.args="args1 args2" -Dexec.classpathScope=runtime


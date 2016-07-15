#Notes on set up deep learning environment


##Hardware 
- CPU i7 6700K
- MotherBoard, ASUS, MAXIMUS VIII RANGER
- Graphics card, GTX 1080, 索泰 至尊 plus
- Memory, 16G
- SSD, 256G
- Hard disc, 2T


## 操作系统， Windows 12, Ubuntu 16.04 双系统
- 使用EasyBCD做双系统引导。

- 安装ubuntu的时候，记得要切换到核显，否则安装的时候是黑屏，GTX 1080已经没有VGA输出接口。BIOS显示设置从Auto修改到IGFX，别忘了显示器接线从显卡切换到主板上的显示输出口。

- 隐藏GRUB引导菜单
EasyBCD引导出来后，选择ubuntu，这个时候，grub又来引导一下，很累赘，所以想skip grub menu，修改/etc/default/grub:
```
GRUB_DEFAULT=0
GRUB_TIMEOUT=0
GRUB_TIMEOUT_STYLE=hidden
GRUB_HIDDEN_TIMEOUT=0
GRUB_HIDDEN_TIMEOUT_QUIET=true
GRUB_DISABLE_OS_PROBER=true  #关键是这个参数
```
修改完后，运行
```
$ grub-update
$ reboot
```
grub 引导菜单不再出来。

## ubuntu安装nvidia driver
一开始，直接下载了CUDA 8.0RC安装，装完以后，重新启动，不能登陆。现象是输入密码按回车以后，直接又回到登陆界面。
可能的原因是CUDA安装包中带的驱动（361）和GPU不匹配。

###解决方法：
- 在你的用户登录界面按CTRL+ALT+F1进入TTY模式
- 输入你的账户名和密码
- 依次运行如下语句：

```
$ sudo apt-get purge nvidia*
$ sudo add-apt-repository ppa:graphics-drivers/ppa
$ sudo apt-get update
$ sudo apt-get install nvidia-367
$ reboot
```
//重启

- 重启后问题就可以正常进入系统了，慢着，还没有，

Ubuntu16.04任务栏与启动器消失了

重设compiz设置
compiz是基于 OpenGL的混合型窗口管理器，通俗一点理解，就是可以在Linux桌面系统内提供类似于Vista和Mac OS的3D桌面效果。
使用以下命令：
重置compiz，在桌面上点右键菜单，打开一个terminal，运行：
```
dconf reset -f /org/compiz/
```

ubuntu 里的显卡驱动安装好以后，可以从核显切换回使用显卡了。

## 重新安装CUDA 8.0RC

- 使用run file 安装，里面有更多的安装选项。
安装到缺省路径，
选择不覆盖现有的驱动。

设置路径：
```
$ export PATH=/usr/local/cuda-8.0/bin:$PATH
$ export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64:$LD_LIBRARY_PATH
```

并且把路径添加到.bashrc

- 安装cuDNN v5
下载安装包，解压
```
$ cd folder/extracted/contents
$ sudo cp -P include/cudnn.h /usr/include
$ sudo cp -P lib64/libcudnn* /usr/lib/x86_64-linux-gnu/
$ sudo chmod a+r /usr/lib/x86_64-linux-gnu/libcudnn*
```

- 设置 cnMeM
[lib]
cnmem = 0.9    
//注意是浮点数，如果显示器接在GPU上，显存不能100%用于计算，不能设置1.0，可能试试0.7等等

## 安装 Anaconda3
装完这个后，python常用的东西就都有了，包含了spyder


## 安装 keras, theano
```
$ pip install keras
```
这个比较顺利，装完之后可以运行 
```
>>> import theano
```
测试一下。

修改~/.theanorc
```
[cuda]
root = /usr/local/cuda-8.0

[global]
device = gpu0
floatX = float32
```
等等一些运行中常用的配置，都可以放在这里。

测试运行了一下keras/examples/mnist_cnn.py
结果还是比较满意，GTX 1080很强大。
###测试结果
- Windows 7, i5 laptop                      ：           20 m / epoch
- Windows 10,  i7 6700k                    ：           2 m / epoch
- Windows 10, GPU GTX 1080            ：           6s / epoch
- Ubuntu 16, GPU GTX 1080                 ：      2s / epoch

cuDNN影响很大，有cuDNN速度要提高一倍左右。

还跑了一下nbody:
```
$ ./nbody -benchmark -numbodies=256000
```
ubuntu 16: 5900 Gflop/s, windows 10: 4800 Gflop/s

## 安装Tensorflow
Tensorflow是要重点研究的，以后大部分的工作会在Tensorflow上做，其它的用来比较。CNTK虽然有一点速度的优势，但是介于配置和脚本之间的brainscript还是不舒服，直接用python表达比较方便。
另一方面还是基于对Google的信任。
接下来安装Tensorflow。。。

Tensorflow从源代码安装，因为要支持新版本的cuDNN。
Bazel安装好了。
Bazel设计的不错，模型很干净，下次可以在项目中用。

Github 不给力啊，速度太慢了，而且老是断，没法玩了。。必须上VPN了。


## 安装无线网卡
8192eu 芯片

[http://blog.csdn.net/hobertony_7/article/details/45071875](http://blog.csdn.net/hobertony_7/article/details/45071875)  
[https://sites.google.com/site/easylinuxtipsproject/reserve-7](https://sites.google.com/site/easylinuxtipsproject/reserve-7)  

wicd 打开后能扫描出wifi热点，能通过密码认证，但是在obtaining IP address。。。一直没有返回，还要继续折腾。。。

上面帖子中的这个驱动还是work的， 能上网了，设置了静态IP。

USB无线网卡搞了太长时间，下次要用linux就上pci的。




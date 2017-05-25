# naive 的图书信息录入工具

1. 用 QQ 手机客户端扫书的条形码得到带 isbn 信息的链接
2. 加入到程序列表或文件列表中
3. 正则取出 isbn 字串
4. 通过查询亚马逊得到图书基本信息
5. 存入到 csv 中


运行方法
```shell
python3.6 -c 'from isbn.spiders import amazon; amazon.main()'
```


TODO:
+ [x] 链接列表文件 / isbn 列表文件
+ [ ] isbn 查询结果只保留一个
+ [ ] 错误处理
+ [x] isbn group 正则
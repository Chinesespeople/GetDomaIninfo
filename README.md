# GetDomaIninfo
 批量获取域名备案信息


默认爬取当前目录中的test.txt文件中的域名。

```bash
usage: getdomaininfo.py [-h] [--file FILE] [--output OUTPUT]
                        [--threads THREADS]

Get Domain Information

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  设置一个域名列表文件，该文件每一行应该为一个域名格式的字符串。默认为当前目录下的test.txt。
  --output OUTPUT, -o OUTPUT
                        指定输出的csv文件名。不指定该参数程序将会将结果默认保存为[当前时间戳.csv]文件。
  --threads THREADS, -t THREADS
                        指定线程数。默认为 1。
```
                        

![image](https://github.com/Chinesespeople/GetDomaIninfo/assets/42881938/16c388ee-e668-422c-b131-4d362d9e8908)

分别对应的是[百度权重、域名、单位名称、单位性质、备案号、IP地址]

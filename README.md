####搜狐题目
#####编写一个程序，每60秒抓取m.sohu.com这个页面一次，并把相应的文件备份到/tmp/backup下，图片备份到img下，js文件备份到js下，css文件备份到css文件下，在本地打开要和线上效果一致。
#####程序缺点：没有实现css里面图片的提取。
#####调用方式：main.py -d 60 -u http://www.m.sohu.com -o /tmp/backup

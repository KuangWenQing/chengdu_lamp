### 成都董家湾路灯项目概述
1. true_pos_extract 下的代码用来得到真值坐标，正值见表 lamp_information.xlsx
2. data_analysis 下的代码用来分析成都给的表格数据， 执行 excel_analysis.py
3. position_compare 下的代码用来比较1.真值 和 2. 步中的分析后数据

## <font color=red>注意， 1. 已经完成， 不要再执行 true_pos_extract 中的代码</font>


### 1. true_pos_extract 路径详解
+ 每盏灯的位置都有u-center 的定位界面截图，QQ拼音截图会自动以系统时间命名。
+ 根据截图的图片名字中的时间提取 对应时刻的 GGA 语句， 从而得到该路灯的位置。代码实现见 picture_name_list.py
+ all_lamp_information_table.py  将所有路灯的信息（编号，位置）汇总成表。
+ 董家湾所有路灯信息汇总表见 lamp_information.xlsx


### 2. data_analysis 路径详解
+ 每一盏灯都会有一个表格文件，表格每一行记录着当前时刻的内存信息（内存有位置，信噪比，中断数...详见唐煌的C代码结构体）
+ <font color=red>注意：表格行数越小，其时间离当前UTC越近
+ *hexContent* 列是二进制字符串，部分二进制对应C语言结构体的内存</font>
+ 目前 '47 50 53 3A ' 之后二进制对应 C语言的结构体
+ excel_analysis.py 会调用 parser_str_bin 来解析二进制字符串
+ 然后 调用 gga_produce 构建 GGA语句
+ 同时根据时间将构建的 GGA分别写入文件，共以下三种方式：
+ 每一天存一个gga文件，每一天最后一条GGA存一个文件， 所有gga存一个文件 
+ 最后把gga文件转换成Google地球可识别的kml文件，归档各个文件到不同文件夹。


### 3. position_compare 路径详解
+ last_gga_analysis.py 遍历 以年月日命名的文件夹， 计算每天最后一条GGA的误差，写表
+ whole_gga_analysis.py 遍历 whole_gga 文件夹，  计算所有时刻定位的误差，画图
+ last_AVE_analysis.py 用来计算 log文件中最后一条 'DEBUG R AVE,' 的位置误差。
+ 该log文件是由spi输出的二进制文件转换而来。 转换工具是 *bin2log_rely_xml*
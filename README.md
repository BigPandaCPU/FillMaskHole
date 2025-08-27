# 对mask中的孔洞进行填充
    该方法只对凸的mask有效，需要谨慎使用

## 原理简介
    通过在X,Y,Z 三个方向上，提取每个切片，进行二维轮廓提取，对轮廓中的部分进行填充。

## 填充结果
![image](data/对比结果.png)


## 过填充
![image](data/过填充.png)

## 运行
python -i ./data/CT_hip.nrrd -o ./data/CT_hip_fill.nrrd -d Z
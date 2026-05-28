import dat

model = dat.Model()

# 计算余弦距离
print(model.distance("猫", "狗"))   # 0.42167168697997226
print(model.distance("猫", "长城")) # 0.7688800132250979

# 计算DAT分数
print(model.dat(["猫", "狗"], 2))   # 42.167168697997226
print(model.dat(["猫", "长城"], 2)) # 76.8880013225098

# 词语示例
low = ["书", "书桌", "杯子", "窗户", "座椅", "鞋子", "大门"]
average = ["云朵", "石头", "月亮", "风", "梦", "星光", "面包"]
high = ["鲸鱼", "极光", "长城", "陨石", "高山", "万有引力", "宇宙"]

# 计算DAT分数
print(model.dat(low))   # 69.24429404399925
print(model.dat(average))   # 70.35311887033055
print(model.dat(high))  # 72.3271017774138

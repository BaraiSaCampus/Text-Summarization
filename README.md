# flaskProject
#gene.py中导入的预训练模型需要自行配置，可以替换为其他已有模型

#我用的预训练模型是palm，训练参数如下
train_epochs=15
max_sequence_length=128
batch_size=8
learning_rate=1e-3
optimizer=AdamW

## 背景介绍
IAAS自动部署系统，接收来自云翼的上线请求，将请求信息持久化到数据库中，转发请求到后端MQ

## 服务接口说明
- Swagger API: <URL>/docs/
- 例如：http://adstest.pga.iaas.jcloud.com/docs/

## 编译构建
- 构建Docker镜像
```
docker build .
```

## 单元测试
```
bash unittest.sh
```

## 本地开发启动服务
```
bash dev-start.sh
```

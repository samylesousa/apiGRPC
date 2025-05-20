# API GRPC
A seguinte API tem como objetivo ser a aplicação intermediária para um site de divulgação de oportunidades (cursos, estágios e bolsas acadêmicas) e um banco de dados que contém as informações sobre tais oportunidades.

### Bibliotecas utilizadas no projeto
* asyncmy (driver mysql)
* grpcio (pacote para o grpc em python)
* grpcio-tools (pacote para o grpc em python)
* sqlalchemy (toolkit para o banco de dados)


### Como rodar o projeto

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dados.proto

* python -m grpc_tools.protoc (comando para rodar o compilador)
* dados.proto (o arquivo protocol buffers)

python server.py

python client.py
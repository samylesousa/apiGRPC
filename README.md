API GRPC
A seguinte API tem como objetivo ser a aplicação intermediária para um site de divulgação de oportunidades (cursos, estágios e bolsas acadêmicas) e um banco de dados que contém as informações sobre tais oportunidades.

### Bibliotecas utilizadas no projeto
* asyncmy (driver mysql)
* grpcio (pacote para o grpc em python)
* grpcio-tools (pacote para o grpc em python)
* sqlalchemy (toolkit para o banco de dados)


### Como rodar o projeto
1. python -m venv env
2. env\Scripts\Activate.ps1
3. python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. dados.proto
4. python server.py
5. python client.py

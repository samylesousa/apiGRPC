import grpc

def createEnderecosImport(stub, dados_pb2, request): 
    try:
        endereco_criado = stub.CreateEndereco(dados_pb2.CreateEnderecoRequest(
            rua=request["rua"],
            numero=request["numero"] if "numero" in request else None,
            bairro=request["bairro"] if "bairro" in request else None,
            cidade=request["cidade"] if "cidade" in request else None,
            estado=request["estado"] if "estado" in request else None,
            cep=request["cep"] if "cep" in request else None,
        ))
        print(f'Endereco criado:{endereco_criado.rua} (ID: {endereco_criado.id})')
    except grpc.RpcError as e:
        print(f"Erro ao criar os endereços: {e.code()}: {e.details()}")
    return


def getAllEnderecosImport(stub, dados_pb2):
    try:
        todos_enderecos = stub.ListEnderecos(dados_pb2.ListEnderecoRequest())
        for endereco in todos_enderecos.enderecos:
            print(f"{endereco.id}: {endereco.rua} - {endereco.cidade}")
    except grpc.RpcError as e:
        print(f"Erro ao listar os enderecos:{e.code()}: {e.details()}")


def getEnderecosElementImport(stub, dados_pb2, request):
    try:
        enderecos_filtrados = stub.ListEnderecos(dados_pb2.ListEnderecoRequest(cidade=request['cidade']))
        for endereco in enderecos_filtrados.enderecos:
            print(f"Filtrado: {endereco.id}: {endereco.rua} - {endereco.cidade}")
    except grpc.RpcError as e:
        print(f"Erro ao filtrar endereços: {e.code(): {e.details()}}")

def getEnderecoIdImport(stub, dados_pb2, request):
    try:
        endereco_especifico = stub.GetEndereco(dados_pb2.EnderecoRequest(id=request['id']))
        print(f"Endereço {endereco_especifico.id}: {endereco_especifico.rua}")
    except grpc.RpcError as e:
        print(f"Erro ao obter endereço: {e.code(): {e.details()}}")
    

def updateEnderecoImport(stub, dados_pb2, request):
    try:
        endereco_atualizado = stub.UpdateEndereco(dados_pb2.Endereco(
            id=request['id'],
            rua=request['rua'] if "rua" in request else None,
            numero=request["numero"] if "numero" in request else None,
            bairro=request["bairro"] if "bairro" in request else None,
            cidade=request["cidade"] if "cidade" in request else None,
            estado=request["estado"] if "estado" in request else None,
            cep=request["cep"] if "cep" in request else None,
        ))
        print(f"Endereço atualizado: {endereco_atualizado.rua}")
    except grpc.RpcError as e:
        print(f"Erro ao atualizar o endereço: {e.code()}: {e.details()}")

def deleteEnderecoImport(stub, dados_pb2, request):
    try:
        stub.DeleteEndereco(dados_pb2.EnderecoRequest(id=request['id']))
        print(f"Endereço deletado")
    except grpc.RpcError as e:
        print(f"Erro ao deletar a tarefa: {e.code()}: {e.details()}")
    
    # #verifiando lista após deletar o endereço
    # #esse método está pronto
    # print("\nLista de endereços:")
    # try:
    #     enderecos_finais = stub.ListEnderecos(dados_pb2.ListEnderecoRequest())
    #     for endereco in enderecos_finais.enderecos:
    #         print(f"{endereco.id}: {endereco.rua} - {endereco.cidade}")
    # except grpc.RpcError as e:
    #     print(f"Erro ao listar endereços finais: {e.code(): {e.details()}}")
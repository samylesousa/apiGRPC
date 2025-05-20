import grpc

def createPlataformaImport(stub, dados_pb2, request):
    try:
        plataforma = stub.CreatePlataforma(dados_pb2.CreatePlataformaRequest(
            nome=request["nome"],
            email=request["email"] if "email" in request else None,
            website=request["website"],
            tipo=request["tipo"]
        ))
        print(f'Nome: {plataforma.nome} Plataforma criada:{plataforma.email} (Website: {plataforma.website})')
    except grpc.RpcError as e:
        print(f"Erro ao criar a plataforma: {e.code()}: {e.details()}")
        return        
       

def getAllPlataformasImport(stub, dados_pb2):
    try:
        todas_plataformas = stub.ListPlataformas(dados_pb2.ListPlataformasRequest())
        for plataforma in todas_plataformas.plataformas:
            print(f'Nome: {plataforma.nome} Email:{plataforma.email} (Website: {plataforma.website})')
    except grpc.RpcError as e:
        print(f"Erro ao listar as plataformas:{e.code()}: {e.details()}")
        
def getPlataformaElementImport(stub, dados_pb2, request):
    try:
        #falta adicionar a parte de estados
        plataformas_filtradas = stub.ListPlataformas(dados_pb2.ListPlataformasRequest(tipo=request["tipo"]))
        for plataforma in plataformas_filtradas.plataformas:
            print(f'Nome: {plataforma.nome} Email:{plataforma.email} (Website: {plataforma.website})')
    except grpc.RpcError as e:
        print(f"Erro ao filtrar as plataformas: {e.code(): {e.details()}}")
        
def getPlataformaIdImport(stub, dados_pb2, request):
    try:
        plataforma_especifica = stub.GetPlataforma(dados_pb2.PlataformaRequest(id=request["id"]))
        print(f'Nome: {plataforma_especifica.nome} Email:{plataforma_especifica.email} (Website: {plataforma_especifica.website})')
    except grpc.RpcError as e:
        print(f"Erro ao obter a plataforma: {e.code(): {e.details()}}")


def updatePlataformaImport(stub, dados_pb2, request):
    try:
        plataforma_atual = stub.UpdatePlataforma(dados_pb2.Plataforma(
            id=request["id"],
            nome=request["nome"] if "nome" in request else None,
            email=request["email"] if "email" in request else None,
            website=request["website"] if "website" in request else None,
            tipo=request["tipo"] if "tipo" in request else None,
        ))
        print(f"Plataforma atualizada: {plataforma_atual.nome}")
    except grpc.RpcError as e:
        print(f"Erro ao atualizar a plataforma: {e.code()}: {e.details()}")


def deletePlataformaImport(stub, dados_pb2, request):
    try:
        stub.DeletePlataforma(dados_pb2.PlataformaRequest(id=request["id"]))
        print(f"Plataforma deletada")
    except grpc.RpcError as e:
        print(f"Erro ao deletar a plataforma: {e.code()}: {e.details()}")




    # #verifiando lista após deletar o endereço
    # #esse método está pronto
    # print("\nLista de endereços:")
    # try:
    #     enderecos_finais = stub.ListEnderecos(dados_pb2.ListEnderecoRequest())
    #     for endereco in enderecos_finais.enderecos:
    #         print(f"{endereco.id}: {endereco.rua} - {endereco.cidade}")
    # except grpc.RpcError as e:
    #     print(f"Erro ao listar endereços finais: {e.code(): {e.details()}}")
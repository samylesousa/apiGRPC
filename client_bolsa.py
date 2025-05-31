import grpc

def createBolsaImport(stub, dados_pb2, request):
    try:
        bolsa_criada = stub.CreateBolsa(dados_pb2.CreateBolsaRequest(
            nome=request["nome"],
            vertente=request["vertente"] if "vertente" in request else None,
            salario=request["salario"] if "salario" in request else None,
            remunerado=request["remunerado"] if "remunerado" in request else None,
            horas_semanais=request["horas_semanais"] if "horas_semanais" in request else None,
            quantidade_vagas=request["quantidade_vagas"] if "quantidade_vagas" in request else None,
            descricao=request["descricao"] if "descricao" in request else None,
            data_inicio=request["data_inicio"] if "data_inicio" in request else "0000-00-00",
            data_fim=request["data_fim"] if "data_fim" in request else "0000-00-00",
            professor_id=request["professor_id"] if "professor_request" in request else None
        ))
        print(f'Nome: {bolsa_criada.nome} Bolsa criada:{bolsa_criada.vertente} (Horas Semanais: {bolsa_criada.horas_semanais})')
    except grpc.RpcError as e:
        print(f"Erro ao criar a bolsa: {e.code()}: {e.details()}")
        return        
       

def getAllBolsasImport(stub, dados_pb2):
    try:
        todas_bolsas = stub.ListBolsas(dados_pb2.ListBolsasRequest())
        for bolsa in todas_bolsas.bolsas:
            print(f'Nome: {bolsa.nome} Vertente:{bolsa.vertente}')
    except grpc.RpcError as e:
        print(f"Erro ao listar as bolsas:{e.code()}: {e.details()}")
        
# def getBolsaElementImport(stub, dados_pb2, request):
#     try:
#         #falta adicionar a parte de remunerado e horas_semanais
#         bolsas_filtradas = stub.ListBolsas(dados_pb2.ListBolsasRequest(vertente=request["vertente"]))
#         for bolsa in bolsas_filtradas.bolsas:
#             print(f'Nome: {bolsa.nome} Vertente:{bolsa.vertente}')
#     except grpc.RpcError as e:
#         print(f"Erro ao filtrar as bolsas: {e.code(): {e.details()}}")
        
def getBolsaIdImport(stub, dados_pb2, request):
    try:
        bolsa_especifica = stub.GetBolsa(dados_pb2.BolsaRequest(id=request["id"]))
        print(f'Nome: {bolsa_especifica.nome} Vertente:{bolsa_especifica.vertente}')
    except grpc.RpcError as e:
        print(f"Erro ao obter a bolsa específica: {e.code(): {e.details()}}")


def updateBolsaImport(stub, dados_pb2, request):
    try:
        bolsa_atual = stub.UpdateBolsa(dados_pb2.Bolsa(
            id=request["id"],
            nome=request["nome"] if "nome" in request else None,
            vertente=request["vertente"] if "vertente" in request else None,
            salario=request["salario"] if "salario" in request else None,
            remunerado=request["remunerado"] if "remunerado" in request else None,
            horas_semanais=request["horas_semanais"] if "horas_semanais" in request else None,
            quantidade_vagas=request["quantidade_vagas"] if "quantidade_vagas" in request else None,
            descricao=request["descricao"] if "descricao" in request else None,
            data_inicio=request["data_inicio"] if "data_inicio" in request else None,
            data_fim=request["data_fim"] if "data_fim" in request else None,
            professor_id=request["professor_id"] if "professor_request" in request else None
        ))
        print(f"Bolsa atualizada: {bolsa_atual.nome}")
    except grpc.RpcError as e:
        print(f"Erro ao atualizar a bolsa: {e.code()}: {e.details()}")


def deleteBolsaImport(stub, dados_pb2, request):
    try:
        stub.DeleteBolsa(dados_pb2.BolsaRequest(id=request["id"]))
        print(f"Bolsa deletada")
    except grpc.RpcError as e:
        print(f"Erro ao deletar a bolsa: {e.code()}: {e.details()}")




    # #verifiando lista após deletar o endereço
    # #esse método está pronto
    # print("\nLista de endereços:")
    # try:
    #     enderecos_finais = stub.ListEnderecos(dados_pb2.ListEnderecoRequest())
    #     for endereco in enderecos_finais.enderecos:
    #         print(f"{endereco.id}: {endereco.rua} - {endereco.cidade}")
    # except grpc.RpcError as e:
    #     print(f"Erro ao listar endereços finais: {e.code(): {e.details()}}")
import asyncio
import grpc
import dados_pb2
import dados_pb2_grpc
from client_endereco import createEnderecosImport, getAllEnderecosImport, getEnderecoIdImport, updateEnderecoImport, deleteEnderecoImport
from client_plataforma import createPlataformaImport, getAllPlataformasImport, getPlataformaIdImport, updatePlataformaImport, deletePlataformaImport
from client_professor import createProfessorImport, getAllProfessoresImport, getProfessorIdImport, updateProfessorImport, deleteProfessorImport, getProfessorElementImport
from client_bolsa import createBolsaImport, getAllBolsasImport, getBolsaIdImport, updateBolsaImport, deleteBolsaImport, getBolsaElementImport


options = [
    ('grpc.max_receive_message_length', 50 * 1024 * 1024),  # 50 MB, por exemplo
]
channel = grpc.insecure_channel('localhost:50051', options=options)

async def run():
    async with grpc.aio.insecure_channel('localhost:50051'):
        # stub = dados_pb2_grpc.EnderecoServiceStub(channel)

        # request = {"rua": 'Almeida Ferreiro', "numero": 300, "bairro": 'centro'}
        # createEnderecosImport(stub, dados_pb2, request)
        # getAllEnderecosImport(stub, dados_pb2)
        # getEnderecoIdImport(stub, dados_pb2, {'id': 89})
        # updateEnderecoImport(stub, dados_pb2, {"id": 35527, "rua": "Anahid de Andrade"})
        # deleteEnderecoImport(stub, dados_pb2, {"id": 35519})

        # stub = dados_pb2_grpc.PlataformaServiceStub(channel)

        # request = {"nome": 'Youtube', "website": "youtube.com", "tipo": 1}
        # createPlataformaImport(stub, dados_pb2, request)
        # getAllPlataformasImport(stub, dados_pb2)
        # getPlataformaIdImport(stub, dados_pb2, {'id': 89})
        # updatePlataformaImport(stub, dados_pb2, {"id": 39701, "nome": "Youtube Premium"})
        # deletePlataformaImport(stub, dados_pb2, {"id": 39701})

        # stub = dados_pb2_grpc.ProfessorServiceStub(channel)

        # request = {"nome": 'Eduardo Silva', "website": "eduardosilva.com", "email": "eduardolsilva@gmail.com"}
        # createProfessorImport(stub, dados_pb2, request)
        # getAllProfessoresImport(stub, dados_pb2)
        # getProfessorElementImport(stub, dados_pb2, {"vertente": "Telecomunicações"})
        # getProfessorIdImport(stub, dados_pb2, {'id': 90})
        # updateProfessorImport(stub, dados_pb2, {"id": 40311, "nome": "Eduardo Augusto"})
        # deleteProfessorImport(stub, dados_pb2, {"id": 40311})

        stub = dados_pb2_grpc.BolsaServiceStub(channel)

        # request = {"nome": 'Monitoria de Química', "vertente": "Telecomunicações"}
        # createBolsaImport(stub, dados_pb2, request)
        # getBolsaElementImport(stub, dados_pb2, {"vertente": "Telecomunicações"})
        # getAllBolsasImport(stub, dados_pb2)
        getBolsaIdImport(stub, dados_pb2, {'id': 90})
        # updateBolsaImport(stub, dados_pb2, {"id": 8820, "nome": "Monitoria de Física"})


        # deleteBolsaImport(stub, dados_pb2, {"id": 8820})


    #     #criando enderecos (POST)
    #     #esse método já ta correto
    #     print("criando enderecos")
    #     try:
    #         endereco1 = stub.CreateEndereco(dados_pb2.CreateEnderecoRequest(
    #             rua="Anahid de Andrade",
    #             numero=195,
    #             bairro="Centro",
    #             cidade="Sobral",
    #             estado="CE",
    #             cep="83949484",
    #         ))
    #         print(f'Endereco criado:{endereco1.rua} (ID: {endereco1.id})')
    #     except grpc.RpcError as e:
    #         print(f"Erro ao criar os endereços: {e.code()}: {e.details()}")
    #         return
        
    #     #listando todos os enderecos
    #     #esses métodos estão corretos
    #     print("\nEndereços:")
    #     try:
    #         todos_enderecos = stub.ListEnderecos(dados_pb2.ListEnderecoRequest())
    #         for endereco in todos_enderecos.enderecos:
    #             print(f"{endereco.id}: {endereco.rua} - {endereco.cidade}")
    #     except grpc.RpcError as e:
    #         print(f"Erro ao listar os enderecos:{e.code()}: {e.details()}")

    #     #listando os enderecos por cidade
    #     print("\nEndereços por cidade:")
    #     try:
    #         enderecos_filtrados = stub.ListEnderecos(dados_pb2.ListEnderecoRequest(cidade="Sobral"))
    #         for endereco in enderecos_filtrados.enderecos:
    #             print(f"Filtrado: {endereco.id}: {endereco.rua} - {endereco.cidade}")
    #     except grpc.RpcError as e:
    #         print(f"Erro ao filtrar endereços: {e.code(): {e.details()}}")


    # #obtendo um endereço específico
    # #esse método já ta correto
    # print("\nEndereço específico:")
    # try:
    #     endereco_especifico = stub.GetEndereco(dados_pb2.EnderecoRequest(id=8))
    #     print(f"Endereço {endereco_especifico.id}: {endereco_especifico.rua}")
    # except grpc.RpcError as e:
    #     print(f"Erro ao obter endereço: {e.code(): {e.details()}}")
    

    # #atualizando um endereço
    # #esse método está correto
    # print("\nAtualizando endereço:")
    # try:
    #     endereco_atualizado = stub.UpdateEndereco(dados_pb2.Endereco(
    #         id=9,
    #         rua="Anahid de Andrade"
    #     ))
    #     print(f"Endereço atualizado: {endereco_atualizado.rua}")
    # except grpc.RpcError as e:
    #     print(f"Erro ao atualizar o endereço: {e.code()}: {e.details()}")

    # #deletando um endereço
    # #esse método já ta correto
    # print("\nDeletando Endereço")
    # try:
    #     stub.DeleteEndereco(dados_pb2.EnderecoRequest(id=98))
    #     print(f"Endereço deletado")
    # except grpc.RpcError as e:
    #     print(f"Erro ao deletar a tarefa: {e.code()}: {e.details()}")
    
    # #verifiando lista após deletar o endereço
    # #esse método está pronto
    # print("\nLista de endereços:")
    # try:
    #     enderecos_finais = stub.ListEnderecos(dados_pb2.ListEnderecoRequest())
    #     for endereco in enderecos_finais.enderecos:
    #         print(f"{endereco.id}: {endereco.rua} - {endereco.cidade}")
    # except grpc.RpcError as e:
        # print(f"Erro ao listar endereços finais: {e.code(): {e.details()}}")

if __name__ == '__main__':
    asyncio.run(run())

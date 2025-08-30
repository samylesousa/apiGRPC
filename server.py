import grpc
from concurrent import futures
import dados_pb2
import dados_pb2_grpc
from database.models import EmpresaModel, CursoModel, EstagioModel, BolsaModel, ProfessorModel, PlataformaModel, EnderecoModel
from database.database_config import get_session
import asyncio
from sqlalchemy import select, update, delete

#classes para os elementos do .proto
class EnderecoService(dados_pb2_grpc.EnderecoServiceServicer):

    async def GetEndereco(self, request, context):
        async with get_session() as session:
            item = await session.get(EnderecoModel, request.id)

            if item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Item Indisponível")
                return dados_pb2.Endereco()

            return dados_pb2.Endereco(
                id=item.id,
                rua=item.rua,
                numero=item.numero,
                bairro=item.bairro,
                cidade=item.cidade,
                estado=item.estado,
                cep=item.cep
            )

    async def CreateEndereco(self, request, context):
        async with get_session() as session:
            try:
                novo_item = EnderecoModel(
                    rua=request.rua,
                    numero=request.numero,
                    bairro=request.bairro,
                    cidade=request.cidade,
                    estado=request.estado,
                    cep=request.cep
                )
                session.add(novo_item)
                await session.commit()
                await session.refresh(novo_item)

                return dados_pb2.Endereco(
                    id=novo_item.id,
                    rua=novo_item.rua,
                    numero=novo_item.numero,
                    bairro=novo_item.bairro,
                    cidade=novo_item.cidade,
                    estado=novo_item.estado,
                    cep=novo_item.cep,
                    success=True
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Endereco(success=False)

    async def ListEnderecos(self, request: dados_pb2.ListEnderecoRequest, context):
        async with get_session() as session:

            resultado = await session.execute(select(EnderecoModel))
            enderecos = resultado.scalars().all()

            lista_enderecos = dados_pb2.EnderecoListResponse()
            for endereco in enderecos:
                lista_enderecos.enderecos.append(
                    dados_pb2.Endereco(
                        id=endereco.id,
                        rua=endereco.rua,
                        bairro=endereco.bairro,
                        cidade=endereco.cidade,
                        estado=endereco.estado,
                        cep=endereco.cep
                    )
                )
            return lista_enderecos

    async def UpdateEndereco(self, request: dados_pb2.Endereco, context):
        async with get_session() as session:
            try:
                endereco_existente = await session.get(EnderecoModel, request.id)

                if endereco_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Endereço Indisponível")
                    return dados_pb2.Endereco()

                #atualizando o endereco
                for key, value in request:
                    if key != "id" and value is not None:
                        setattr(endereco_existente, key, value)

                await session.commit()
                await session.refresh(endereco_existente)

                return dados_pb2.Endereco(
                    id=endereco_existente.id,
                    rua=endereco_existente.rua,
                    numero=endereco_existente.numero,
                    bairro=endereco_existente.bairro,
                    cidade=endereco_existente.cidade,
                    estado=endereco_existente.estado,
                    cep=endereco_existente.cep
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Endereco()

    async def DeleteEndereco(self, request: dados_pb2.EnderecoRequest, context):
        async with get_session() as session:
            try:
                endereco_existente = await session.get(EnderecoModel, request.id)

                if endereco_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Endereço Indisponível")
                    return dados_pb2.Empty()

                await session.delete(endereco_existente)
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()

class PlataformaService(dados_pb2_grpc.PlataformaServiceServicer):

    async def GetPlataforma(self, request, context):
        async with get_session() as session:
            item = await session.get(PlataformaModel, request.id)

            if item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Item Indisponível")
                return dados_pb2.Plataforma()

            return dados_pb2.Plataforma(
                id=item.id,
                nome=item.nome,
                email=item.email,
                website=item.website,
                tipo=item.tipo
            )

    async def CreatePlataforma(self, request, context):
        async with get_session() as session:
            try:
                novo_item = PlataformaModel(
                    nome=request.nome,
                    email=request.email,
                    website=request.website,
                    tipo=request.tipo
                )
                session.add(novo_item)
                await session.commit()
                await session.refresh(novo_item)

                return dados_pb2.Plataforma(
                    id=novo_item.id,
                    nome=novo_item.nome,
                    email=novo_item.email,
                    website=novo_item.website,
                    tipo=novo_item.tipo,
                    success=True
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Plataforma(success=False)

    async def ListPlataformas(self, request: dados_pb2.ListPlataformasRequest, context):
        async with get_session() as session:
            resultado = await session.execute(select(PlataformaModel))
            plataformas = resultado.scalars().all()

            lista_plataformas = dados_pb2.PlataformaListResponse()
            for plataforma in plataformas:
                lista_plataformas.plataformas.append(
                    dados_pb2.Plataforma(
                        id=plataforma.id,
                        nome=plataforma.nome,
                        email=plataforma.email,
                        website=plataforma.website,
                        tipo=plataforma.tipo,
                    )
                )
            return lista_plataformas

    async def UpdatePlataforma(self, request: dados_pb2.Plataforma, context):
        async with get_session() as session:
            try:
                plataforma_existente = await session.get(PlataformaModel, request.id)

                if plataforma_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Plataforma Indisponível")
                    return dados_pb2.Plataforma()

                #atualizando o endereco
                for key, value in request:
                    if key != "id" and value is not None:
                        setattr(plataforma_existente, key, value)

                await session.commit()
                await session.refresh(plataforma_existente)


                return dados_pb2.Plataforma(
                    id=plataforma_existente.id,
                    nome=plataforma_existente.nome,
                    email=plataforma_existente.email,
                    website=plataforma_existente.website,
                    tipo=plataforma_existente.tipo

                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Plataforma()

    async def DeletePlataforma(self, request: dados_pb2.PlataformaRequest, context):
        async with get_session() as session:
            try:
                plataforma_existente = await session.get(PlataformaModel, request.id)

                if plataforma_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Plataforma Indisponível")
                    return dados_pb2.Empty()

                #removendo a plataforma
                await session.delete(plataforma_existente)
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()

class ProfessorService(dados_pb2_grpc.ProfessorServiceServicer):

    async def GetProfessor(self, request, context):
        async with get_session() as session:
            item = await session.get(ProfessorModel, request.id)

            if item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Item Indisponível")
                return dados_pb2.Professor()

            return dados_pb2.Professor(
                id=item.id,
                nome=item.nome,
                vertente=item.vertente,
                telefone=item.telefone,
                email=item.email,
                website=item.website,
                formacao=item.formacao
            )

    async def CreateProfessor(self, request, context):
        async with get_session() as session:
            try:
                novo_item = ProfessorModel(
                    nome=request.nome,
                    vertente=request.vertente,
                    telefone=request.telefone,
                    email=request.email,
                    website=request.website,
                    formacao=request.formacao
                )
                session.add(novo_item)
                await session.commit()
                await session.refresh(novo_item)

                return dados_pb2.Professor(
                    id=novo_item.id,
                    nome=novo_item.nome,
                    vertente=novo_item.vertente,
                    telefone=novo_item.telefone,
                    email=novo_item.email,
                    website=novo_item.website,
                    formacao=novo_item.formacao,
                    success=True
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Professor(success=False)

    async def ListProfessores(self, request: dados_pb2.ListProfessoreRequest, context):
        async with get_session() as session:
            resultado = await session.execute(select(ProfessorModel))
            professores = resultado.scalars().all()

            lista_professores = dados_pb2.ProfessorListResponse()
            for professor in professores:
                lista_professores.professores.append(
                    dados_pb2.Professor(
                        id=professor.id,
                        nome=professor.nome,
                        email=professor.email,
                        vertente=professor.vertente,
                        telefone=professor.telefone,
                        website=professor.website,
                        formacao=professor.formacao
                    )
                )
            return lista_professores

    async def UpdateProfessor(self, request: dados_pb2.Professor, context):
        async with get_session() as session:
            try:
                #verificando se o professor existe
                professor_existente = await session.get(ProfessorModel, request.id)

                if professor_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Professor Indisponível")
                    return dados_pb2.Professor()

                #atualizando o professor
                for key, value in request:
                    if key != "id" and value is not None:
                        setattr(professor_existente, key, value)

                await session.commit()
                await session.refresh(professor_existente)

                return dados_pb2.Professor(
                    id=professor_existente.id,
                    nome=professor_existente.nome,
                    vertente=professor_existente.vertente,
                    telefone=professor_existente.telefone,
                    email=professor_existente.email,
                    website=professor_existente.website,
                    formacao=professor_existente.formacao

                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Professor()

    async def DeleteProfessor(self, request: dados_pb2.ProfessorRequest, context):
        async with get_session() as session:
            try:
                #verificando se o professor existe
                professor_existente = await session.get(ProfessorModel, request.id)

                if professor_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Professor Indisponível")
                    return dados_pb2.Empty()

                #removendo o professor
                await session.delete(professor_existente)
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()

class BolsaService(dados_pb2_grpc.BolsaServiceServicer):

    async def GetBolsa(self, request, context):
        async with get_session() as session:
            item = await session.get(BolsaModel, request.id)

            if item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Item Indisponível")
                return dados_pb2.Bolsa()

            return dados_pb2.Bolsa(
                id=item.id,
                nome=item.nome,
                vertente=item.vertente,
                salario=item.salario,
                remunerado=item.remunerado,
                horas_semanais=item.horas_semanais,
                quantidade_vagas=item.quantidade_vagas,
                descricao=item.descricao,
                data_inicio=item.data_inicio,
                data_fim=item.data_fim,
                professor_id=item.professor_id,
            )

    async def CreateBolsa(self, request, context):
        async with get_session() as session:
            try:
                novo_item = BolsaModel(
                    nome=request.nome,
                    vertente=request.vertente,
                    salario=request.salario,
                    remunerado=request.remunerado,
                    horas_semanais=request.horas_semanais,
                    quantidade_vagas=request.quantidade_vagas,
                    descricao=request.descricao,
                    data_inicio=request.data_inicio,
                    data_fim=request.data_fim,
                    professor_id=request.professor_id
                )
                session.add(novo_item)
                await session.commit()
                await session.refresh(novo_item)

                return dados_pb2.Bolsa(
                    id=novo_item.id,
                    nome=novo_item.nome,
                    vertente=novo_item.vertente,
                    salario=novo_item.salario,
                    remunerado=novo_item.remunerado,
                    horas_semanais=novo_item.horas_semanais,
                    quantidade_vagas=novo_item.quantidade_vagas,
                    descricao=novo_item.descricao,
                    data_inicio=novo_item.data_inicio if "data_inicio" in novo_item else None,
                    data_fim=novo_item.data_fim if "data_fim" in novo_item else None,
                    professor_id=novo_item.professor_id,
                    success=True
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Bolsa(success=False)

    async def ListBolsas(self, request: dados_pb2.ListBolsasRequest, context):
        async with get_session() as session:
            resultado = await session.execute(select(BolsaModel))
            bolsas = resultado.scalars().all()

            lista_bolsas = dados_pb2.BolsaListResponse()
            for bolsa in bolsas:
                lista_bolsas.bolsas.append(
                    dados_pb2.Bolsa(
                        id=bolsa.id,
                        nome=bolsa.nome,
                        vertente=bolsa.vertente,
                        salario=bolsa.salario,
                        remunerado=bolsa.remunerado,
                        horas_semanais=bolsa.horas_semanais,
                        quantidade_vagas=bolsa.quantidade_vagas,
                        descricao=bolsa.descricao,
                        data_inicio=bolsa.data_inicio,
                        data_fim=bolsa.data_fim,
                        professor_id=bolsa.professor_id,
                    )
                )
            return lista_bolsas

    async def UpdateBolsa(self, request: dados_pb2.Bolsa, context):
        async with get_session() as session:
            try:
                bolsa_existente = await session.get(BolsaModel, request.id)

                if bolsa_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Bolsa Indisponível")
                    return dados_pb2.Bolsa()

                #atualizando a bolsa
                for key, value in request:
                    if key != "id" and value is not None:
                        setattr(bolsa_existente, key, value)

                await session.commit()
                await session.refresh(bolsa_existente)

                return dados_pb2.Bolsa(
                    id=bolsa_existente.id,
                    nome=bolsa_existente.nome,
                    vertente=bolsa_existente.vertente,
                    salario=bolsa_existente.salario,
                    remunerado=bolsa_existente.remunerado,
                    horas_semanais=bolsa_existente.horas_semanais,
                    quantidade_vagas=bolsa_existente.quantidade_vagas,
                    descricao=bolsa_existente.descricao,
                    data_inicio=bolsa_existente.data_inicio,
                    data_fim=bolsa_existente.data_fim,
                    professor_id=bolsa_existente.professor_id,

                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Bolsa()

    async def DeleteBolsa(self, request: dados_pb2.BolsaRequest, context):
        async with get_session() as session:
            try:
                bolsa_existente = await session.get(BolsaModel, request.id)

                if bolsa_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Bolsa Indisponível")
                    return dados_pb2.Empty()

                await session.delete(bolsa_existente)
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()

class EstagioService(dados_pb2_grpc.EstagioServiceServicer):

    async def GetEstagio(self, request, context):
        async with get_session() as session:

            item = await session.get(EstagioModel, request.id)

            if item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Item Indisponível")
                return dados_pb2.Estagio()

            return dados_pb2.Estagio(
                id=item.id,
                nome=item.nome,
                vertente=item.vertente,
                salario=item.salario,
                remunerado=item.remunerado,
                horas_semanais=item.horas_semanais,
                descricao=item.descricao,
                data_inicio=item.data_inicio,
                data_fim=item.data_fim,
                empresa_id=item.empresa_id,
            )

    async def CreateEstagio(self, request, context):
        async with get_session() as session:
            try:
                novo_item = EstagioModel(
                    nome=request.nome,
                    vertente=request.vertente,
                    salario=request.salario,
                    remunerado=request.remunerado,
                    horas_semanais=request.horas_semanais,
                    descricao=request.descricao,
                    data_inicio=request.data_inicio,
                    data_fim=request.data_fim,
                    empresa_id=request.empresa_id
                )
                session.add(novo_item)
                await session.commit()
                await session.refresh(novo_item)

                return dados_pb2.Estagio(
                    id=novo_item.id,
                    nome=novo_item.nome,
                    vertente=novo_item.vertente,
                    salario=novo_item.salario,
                    remunerado=novo_item.remunerado,
                    horas_semanais=novo_item.horas_semanais,
                    descricao=novo_item.descricao,
                    data_inicio=novo_item.data_inicio,
                    data_fim=novo_item.data_fim,
                    empresa_id=novo_item.empresa_id,
                    success=True
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Estagio(success=False)

    async def ListEstagio(self, request: dados_pb2.ListEstagioRequest, context):
        async with get_session() as session:
            query = select(EstagioModel)
            if request.HasField('vertente'):
                query = select(EstagioModel).where(EstagioModel.vertente == request.vertente)
            if request.HasField('remunerado'):
                query = select(EstagioModel).where(EstagioModel.remunerado == request.remunerado)
            if request.HasField('horas_semanais'):
                query = select(EstagioModel).where(EstagioModel.horas_semanais == request.horas_semanais)

            resultados = await session.execute(query)
            estagios = resultados.scalars().all()

            lista_estagios = dados_pb2.EstagioListResponse()
            for estagio in estagios:
                lista_estagios.estagios.append(
                    dados_pb2.Estagio(
                        id=estagio.id,
                        nome=estagio.nome,
                        vertente=estagio.vertente,
                        salario=estagio.salario,
                        remunerado=estagio.remunerado,
                        horas_semanais=estagio.horas_semanais,
                        descricao=estagio.descricao,
                        data_inicio=estagio.data_inicio,
                        data_fim=estagio.data_fim,
                        empresa_id=estagio.empresa_id,
                    )
                )
            return lista_estagios

    async def UpdateEstagio(self, request: dados_pb2.Estagio, context):
        async with get_session() as session:
            try:
                #verificando se a bolsa existe
                resultado = await session.execute(
                    select(EstagioModel).where(EstagioModel.id == request.id)
                )
                estagio_existente = resultado.scalars().first()

                if estagio_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Estágio Indisponível")
                    return dados_pb2.Estagio()

                #atualizando a bolsa
                await session.execute(
                    update(EstagioModel)
                    .where(EstagioModel.id == request.id)
                    .values(
                        nome=request.nome,
                        vertente=request.vertente,
                        salario=request.salario,
                        remunerado=request.remunerado,
                        horas_semanais=request.horas_semanais,
                        descricao=request.descricao,
                        data_inicio=request.data_inicio,
                        data_fim=request.data_fim,
                        empresa_id=request.empresa_id,
                    )
                )
                await session.commit()

                resultado = await session.execute(
                    select(EstagioModel).where(EstagioModel.id == request.id)
                )
                estagio_atualizado = resultado.scalars().first()

                return dados_pb2.Estagio(
                    id=estagio_atualizado.id,
                    nome=estagio_atualizado.nome,
                    vertente=estagio_atualizado.vertente,
                    salario=estagio_atualizado.salario,
                    remunerado=estagio_atualizado.remunerado,
                    horas_semanais=estagio_atualizado.horas_semanais,
                    descricao=estagio_atualizado.descricao,
                    data_inicio=estagio_atualizado.data_inicio,
                    data_fim=estagio_atualizado.data_fim,
                    empresa_id=estagio_atualizado.empresa_id,

                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Estagio()

    async def DeleteEstagio(self, request: dados_pb2.EstagioRequest, context):
        async with get_session() as session:
            try:
                #verificando se o estágio existe
                resultado = await session.execute(
                    select(EstagioModel).where(EstagioModel.id == request.id)
                )
                estagio_existente = resultado.scalars().first()

                if estagio_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Estágio Indisponível")
                    return dados_pb2.Empty()

                #removendo o estágio
                await session.execute(
                    delete(EstagioModel).where(EstagioModel.id == request.id)
                )
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()

class CursoService(dados_pb2_grpc.CursoServiceServicer):

    async def GetCurso(self, request, context):
        async with get_session() as session:

            item = await session.get(CursoModel, request.id)

            if item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Item Indisponível")
                return dados_pb2.Curso()

            return dados_pb2.Curso(
                id=item.id,
                nome=item.nome,
                categoria=item.categoria,
                preco=item.preco,
                plataforma_id=item.plataforma_id,
                nivel=item.nivel,
                vertente=item.vertente,
                data_inicio=item.data_inicio,
                data_fim=item.data_fim,
            )

    async def CreateCurso(self, request, context):
        async with get_session() as session:
            try:
                novo_item = CursoModel(
                    nome=request.nome,
                    categoria=request.categoria,
                    preco=request.preco,
                    plataforma_id=request.plataforma_id,
                    nivel=request.nivel,
                    vertente=request.vertente,
                    data_inicio=request.data_inicio,
                    data_fim=request.data_fim,
                )
                session.add(novo_item)
                await session.commit()
                await session.refresh(novo_item)

                return dados_pb2.Curso(
                    id=novo_item.id,
                    nome=novo_item.nome,
                    categoria=novo_item.categoria,
                    preco=novo_item.preco,
                    plataforma_id=novo_item.plataforma_id,
                    nivel=novo_item.nivel,
                    vertente=novo_item.vertente,
                    data_inicio=novo_item.data_inicio,
                    data_fim=novo_item.data_fim,
                    success=True
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Curso(success=False)

    async def ListCurso(self, request: dados_pb2.ListCursosRequest, context):
        async with get_session() as session:
            query = select(CursoModel)
            if request.HasField('vertente'):
                query = select(CursoModel).where(CursoModel.vertente == request.vertente)
            if request.HasField('categoria'):
                query = select(CursoModel).where(CursoModel.categoria == request.categoria)
            if request.HasField('nivel'):
                query = select(CursoModel).where(CursoModel.nivel == request.nivel)

            resultados = await session.execute(query)
            cursos = resultados.scalars().all()

            lista_cursos = dados_pb2.CursoListResponse()
            for curso in cursos:
                lista_cursos.cursos.append(
                    dados_pb2.Curso(
                        id=curso.id,
                        nome=curso.nome,
                        categoria=curso.categoria,
                        preco=curso.preco,
                        plataforma_id=curso.plataforma_id,
                        nivel=curso.nivel,
                        vertente=curso.vertente,
                        data_inicio=curso.data_inicio,
                        data_fim=curso.data_fim,
                    )
                )
            return lista_cursos

    async def UpdateCurso(self, request: dados_pb2.Curso, context):
        async with get_session() as session:
            try:
                #verificando se a bolsa existe
                resultado = await session.execute(
                    select(CursoModel).where(CursoModel.id == request.id)
                )
                curso_existente = resultado.scalars().first()

                if curso_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Curso Indisponível")
                    return dados_pb2.Curso()

                #atualizando a bolsa
                await session.execute(
                    update(CursoModel)
                    .where(CursoModel.id == request.id)
                    .values(
                        id=request.id,
                        nome=request.nome,
                        categoria=request.categoria,
                        preco=request.preco,
                        plataforma_id=request.plataforma_id,
                        nivel=request.nivel,
                        vertente=request.vertente,
                        data_inicio=request.data_inicio,
                        data_fim=request.data_fim,
                    )
                )
                await session.commit()

                resultado = await session.execute(
                    select(CursoModel).where(CursoModel.id == request.id)
                )
                curso_atualizado = resultado.scalars().first()

                return dados_pb2.Curso(
                    id=curso_atualizado.id,
                    nome=curso_atualizado.nome,
                    categoria=curso_atualizado.categoria,
                    preco=curso_atualizado.preco,
                    plataforma_id=curso_atualizado.plataforma_id,
                    nivel=curso_atualizado.nivel,
                    vertente=curso_atualizado.vertente,
                    data_inicio=curso_atualizado.data_inicio,
                    data_fim=curso_atualizado.data_fim,

                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Curso()

    async def DeleteCurso(self, request: dados_pb2.CursoRequest, context):
        async with get_session() as session:
            try:
                #verificando se o estágio existe
                resultado = await session.execute(
                    select(CursoModel).where(CursoModel.id == request.id)
                )
                curso_existente = resultado.scalars().first()

                if curso_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Curso Indisponível")
                    return dados_pb2.Empty()

                #removendo o curso
                await session.execute(
                    delete(CursoModel).where(CursoModel.id == request.id)
                )
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()

class EmpresaService(dados_pb2_grpc.EmpresaServiceServicer):

    async def GetEmpresa(self, request, context):
        async with get_session() as session:

            item = await session.get(EmpresaModel, request.id)

            if item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Item Indisponível")
                return dados_pb2.Empresa()

            return dados_pb2.Empresa(
                id=item.id,
                nome=item.nome,
                vertente=item.vertente,
                cnpj=item.cnpj,
                endereco_id=item.endereco_id,
                telefone=item.telefone,
                email=item.email,
                website=item.website,
                status=item.status,
            )

    async def CreateEmpresa(self, request, context):
        async with get_session() as session:
            try:
                novo_item = EmpresaModel(
                    nome=request.nome,
                    vertente=request.vertente,
                    cnpj=request.cnpj,
                    endereco_id=request.endereco_id,
                    telefone=request.telefone,
                    email=request.email,
                    website=request.website,
                    status=request.status,
                )
                session.add(novo_item)
                await session.commit()
                await session.refresh(novo_item)

                return dados_pb2.Empresa(
                    id=novo_item.id,
                    nome=novo_item.nome,
                    vertente=novo_item.vertente,
                    cnpj=novo_item.cnpj,
                    endereco_id=novo_item.endereco_id,
                    telefone=novo_item.telefone,
                    email=novo_item.email,
                    website=novo_item.website,
                    status=novo_item.status,
                    success=True
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empresa(success=False)

    async def ListEmpresa(self, request: dados_pb2.ListEmpresasRequest, context):
        async with get_session() as session:
            query = select(EmpresaModel)
            if request.HasField('vertente'):
                query = select(EmpresaModel).where(EmpresaModel.vertente == request.vertente)

            resultados = await session.execute(query)
            empresas = resultados.scalars().all()

            lista_empresas = dados_pb2.EmpresaListResponse()
            for empresa in empresas:
                lista_empresas.empresas.append(
                    dados_pb2.Empresa(
                        id=empresa.id,
                        nome=empresa.nome,
                        vertente=empresa.vertente,
                        cnpj=empresa.cnpj,
                        endereco_id=empresa.endereco_id,
                        telefone=empresa.telefone,
                        email=empresa.email,
                        website=empresa.website,
                        status=empresa.status,
                    )
                )
            return lista_empresas

    async def UpdateEmpresa(self, request: dados_pb2.Empresa, context):
        async with get_session() as session:
            try:
                #verificando se a empresa existe
                resultado = await session.execute(
                    select(EmpresaModel).where(EmpresaModel.id == request.id)
                )
                empresa_existente = resultado.scalars().first()

                if empresa_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Empresa Indisponível")
                    return dados_pb2.Empresa()

                #atualizando a bolsa
                await session.execute(
                    update(EmpresaModel)
                    .where(EmpresaModel.id == request.id)
                    .values(
                        id=request.id,
                        nome=request.nome,
                        vertente=request.vertente,
                        cnpj=request.cnpj,
                        endereco_id=request.endereco_id,
                        telefone=request.telefone,
                        email=request.email,
                        website=request.website,
                        status=request.status,
                    )
                )
                await session.commit()

                resultado = await session.execute(
                    select(EmpresaModel).where(EmpresaModel.id == request.id)
                )
                empresa_atualizada = resultado.scalars().first()

                return dados_pb2.Empresa(
                        id=empresa_atualizada.id,
                        nome=empresa_atualizada.nome,
                        vertente=empresa_atualizada.vertente,
                        cnpj=empresa_atualizada.cnpj,
                        endereco_id=empresa_atualizada.endereco_id,
                        telefone=empresa_atualizada.telefone,
                        email=empresa_atualizada.email,
                        website=empresa_atualizada.website,
                        status=empresa_atualizada.status,
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empresa()

    async def DeleteEmpresa(self, request: dados_pb2.EmpresaRequest, context):
        async with get_session() as session:
            try:
                #verificando se a empresa existe
                resultado = await session.execute(
                    select(EmpresaModel).where(EmpresaModel.id == request.id)
                )
                empresa_existente = resultado.scalars().first()

                if empresa_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Empresa Indisponível")
                    return dados_pb2.Empty()

                #removendo o curso
                await session.execute(
                    delete(EmpresaModel).where(EmpresaModel.id == request.id)
                )
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()



#iniciando o servidor
async def serve():

    #configurando o servidor o grpc
    servidor = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    dados_pb2_grpc.add_EnderecoServiceServicer_to_server(EnderecoService(), servidor)
    dados_pb2_grpc.add_PlataformaServiceServicer_to_server(PlataformaService(), servidor)
    dados_pb2_grpc.add_ProfessorServiceServicer_to_server(ProfessorService(), servidor)
    dados_pb2_grpc.add_BolsaServiceServicer_to_server(BolsaService(), servidor)
    dados_pb2_grpc.add_EstagioServiceServicer_to_server(EstagioService(), servidor)
    dados_pb2_grpc.add_CursoServiceServicer_to_server(CursoService(), servidor)
    dados_pb2_grpc.add_EmpresaServiceServicer_to_server(EmpresaService(), servidor)
    servidor.add_insecure_port('[::]:50051')
    await servidor.start()
    print("Servidor inicializou na porta 50051")
    await servidor.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())



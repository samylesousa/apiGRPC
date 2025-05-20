#o concurrent.futures é para a execução de chamadas assíncronas
import grpc
from concurrent import futures
import dados_pb2
import dados_pb2_grpc
import asyncio

#imports para o banco de dados
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, update, delete
import asyncmy
#configurando o banco de dados assíncrono
DATABASE_URL = "mysql+asyncmy://root:issoechatopracaralho@localhost:3306/dadosGerais"

#criando uma engine assíncrona
async_engine = create_async_engine(DATABASE_URL, echo=True)

#criando uma fabrica de sessoes assincronas
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

#modelo base para sqlalchemy
Base = sa.orm.declarative_base()

#os modelos abaixo foram os mesmos que eu escrevi para o graphql
#metadados das tabelas para conseguir fazer as requisições
#samyle código
metadata = sa.MetaData()
class EmpresaModel(Base):

    def __init__(self, nome, vertente, cnpj, endereco_id, telefone, email, website, status, **kwargs):
        self.nome = nome
        self.vertente = vertente
        self.cnpj = cnpj
        self.endereco_id = endereco_id
        self.telefone = telefone
        self.email = email
        self.website = website
        self.status = status
    
    def __str__(self):
        return f"""Nome: {self.nome},
            Vertente: {self.vertente},
            CNPJ: {self.cnpj},
            Endereço: {self.endereco_id},
            Telefone: {self.telefone},
            Email: {self.email},
            Website: {self.website},
            Status: {"Ativa" if self.status else "Desativada"}
        """
    __tablename__ = 'empresa'
    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String) 
    vertente = sa.Column(sa.String) 
    cnpj = sa.Column(sa.String)
    endereco_id = sa.Column(sa.Integer, sa.ForeignKey('endereco.id'))
    telefone = sa.Column(sa.String)
    email = sa.Column(sa.String)
    website = sa.Column(sa.String)
    status = sa.Column(sa.Boolean)

    # endereco = sa.orm.relationship("Endereco")

class CursoModel(Base):
    def __init__(self, nome, categoria, preco, plataforma_id, nivel, vertente, data_inicio, data_fim, **kwargs):
        self.nome = nome
        self.vertente = vertente
        self.categoria = categoria
        self.preco = preco
        self.plataforma_id = plataforma_id
        self.nivel = nivel
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def __str__(self):
        return f"""Nome: {self.nome},
            Vertente: {self.vertente},
            Categoria: {self.categoria},
            Preço: {self.preco},
            Plataforma Id: {self.plataforma_id},
            Nível: {self.nivel},
            Data de Início: {self.data_inicio},
            Data de Fim: {self.data_fim}
        """


    __tablename__ = 'curso'
    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    categoria = sa.Column(sa.String)   #se é pago ou não
    preco = sa.Column(sa.Float)
    plataforma_id =  sa.Column(sa.Integer, sa.ForeignKey('plataforma.id'))
    nivel = sa.Column(sa.String)    #as três opções são, iniciante, intermédiario e avançado
    vertente = sa.Column(sa.String)
    data_inicio = sa.Column(sa.DATE)
    data_fim = sa.Column(sa.DATE) 

    # plataforma = sa.orm.relationship("Plataforma")

class EstagioModel(Base):
    def __init__(self, nome, vertente, salario, empresa_id, remunerado, horas_semanais, descricao, data_inicio, data_fim, **kwargs):
        self.nome = nome
        self.vertente = vertente
        self.salario = salario
        self.empresa_id = empresa_id
        self.remunerado = remunerado
        self.horas_semanais = horas_semanais
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def __str__(self):
        return f'''Nome: {self.nome}, 
            Vertente: {self.vertente},
            Salário: {self.salario},
            Empresa Id: {self.empresa_id},
            Remunerado: {"Sim" if self.remunerado else "Não"},
            Horas Semanais: {self.horas_semanais},
            Descrição: {self.descricao},
            Data de Início: {self.data_inicio},
            Data de Fim: {self.data_fim}
        '''


    __tablename__ = 'estagio'
    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    vertente = sa.Column(sa.String)
    salario = sa.Column(sa.Float)
    empresa_id = sa.Column(sa.Integer, sa.ForeignKey('empresa.id'))
    remunerado  = sa.Column(sa.Boolean)
    horas_semanais = sa.Column(sa.Integer)
    descricao = sa.Column(sa.String)
    data_inicio = sa.Column(sa.DATE)
    data_fim = sa.Column(sa.DATE)

    # empresa = sa.orm.relationship("Empresa")

class BolsaModel(Base):
    def __init__(self, nome, vertente, salario, remunerado, horas_semanais, quantidade_vagas, descricao, data_inicio, data_fim, professor_id, **kwargs):
        self.nome = nome
        self.vertente = vertente
        self.salario = salario
        self.remunerado = remunerado
        self.horas_semanais = horas_semanais
        self.quantidade_vagas = quantidade_vagas
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.professor_id = professor_id
    
    def __str__(self):
        return f"""Nome: {self.nome},
            Vertente: {self.vertente},
            Salário: {self.salario},
            Remunerado: {self.remunerado},
            Horas Semanais: {self.horas_semanais},
            Quantidade de Vagas: {self.quantidade_vagas},
            Descrição: {self.descricao},
            Data de Início: {self.data_inicio},
            Data de Fim: {self.data_fim},
            Professor Id: {self.professor_id}
        """


    __tablename__ = 'bolsa'
    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    vertente = sa.Column(sa.String)
    salario = sa.Column(sa.Float)
    remunerado  = sa.Column(sa.Boolean)
    horas_semanais = sa.Column(sa.Integer)
    quantidade_vagas = sa.Column(sa.Integer)
    descricao = sa.Column(sa.String)
    data_inicio = sa.Column(sa.DATE)
    data_fim = sa.Column(sa.DATE) 
    professor_id = sa.Column(sa.Integer, sa.ForeignKey('professor.id'))

    # professor = sa.orm.relationship("Professor")

class ProfessorModel(Base):
    __tablename__ = 'professor'

    def __init__(self, nome, vertente, telefone, email, website, formacao, **kwargs):
        self.nome = nome
        self.vertente = vertente
        self.telefone = telefone
        self.email = email
        self.website = website
        self.formacao = formacao
    
    def __str__(self):
        return f"""Nome: {self.nome}, 
            Vertente: {self.vertente},
            Telefone: {self.telefone},
            Email: {self.email},
            Website: {self.website},
            Formção: {self.formacao}
        """

    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    vertente = sa.Column(sa.String)
    telefone = sa.Column(sa.String)
    email = sa.Column(sa.String)
    website = sa.Column(sa.String)
    formacao = sa.Column(sa.String)

class PlataformaModel(Base):
    def __init__(self, nome, email, website, tipo, **kwargs):
        self.nome = nome
        self.email = email
        self.website = website
        self.tipo = tipo
    
    def __str__(self):
        return f"""Nome: {self.nome},
            Email: {self.email},
            Website: {self.website},
            Tipo: {"Gratuita" if self.tipo else "Paga"}
        """

    __tablename__ = 'plataforma'
    id = sa.Column(sa.Integer, primary_key=True)
    nome = sa.Column(sa.String)
    email = sa.Column(sa.String)
    website = sa.Column(sa.String)
    tipo  = sa.Column(sa.Boolean) #se é paga ou gratuita

class EnderecoModel(Base):
    def __init__(self, rua=None, numero=None, bairro=None, cidade=None, estado=None, cep=None, **kwargs):
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
    
    def __str__(self):
        return f"""Rua: {self.rua},
            Número: {self.numero},
            Bairro: {self.bairro},
            Cidade: {self.cidade},
            Estado: {self.estado},
            Cep: {self.cep}
        """

    __tablename__ = 'endereco'
    id = sa.Column(sa.Integer, primary_key=True)
    rua = sa.Column(sa.String)
    numero = sa.Column(sa.Integer)
    bairro = sa.Column(sa.String) 
    cidade = sa.Column(sa.String)
    estado = sa.Column(sa.String)
    cep = sa.Column(sa.String)
    

#classes para os elementos do .proto
class EnderecoService(dados_pb2_grpc.EnderecoServiceServicer):

    async def GetEndereco(self, request, context):
        async with AsyncSessionLocal() as session:
            #exemplo de consulta assíncrona
            result = await session.execute(
                select(EnderecoModel).where(EnderecoModel.id == request.id)
            )
            item = result.scalars().first()

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
        async with AsyncSessionLocal() as session:
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
        async with AsyncSessionLocal() as session:
            query = select(EnderecoModel)
            if request.HasField('cidade'):
                query = select(EnderecoModel).where(EnderecoModel.cidade == request.cidade)
                # query = query.filter(cidade=request.cidade)
            if request.HasField('estado'):
                # query = query.filter(estado=request.estado)
                query = select(EnderecoModel).where(EnderecoModel.estado == request.estado)

            resultados = await session.execute(query)
            enderecos = resultados.scalars().all()

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
        async with AsyncSessionLocal() as session:
            try:
                #verificando se o endereco existe
                resultado = await session.execute(
                    select(EnderecoModel).where(EnderecoModel.id == request.id)
                )
                endereco_existente = resultado.scalars().first()

                if endereco_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Endereço Indisponível")
                    return dados_pb2.Endereco()
                
                #atualizando o endereco
                await session.execute(
                    update(EnderecoModel)
                    .where(EnderecoModel.id == request.id)
                    .values(
                        rua=request.rua,
                        numero=request.numero,
                        bairro=request.bairro,
                        cidade=request.cidade,
                        estado=request.estado,
                        cep=request.cep
                    )
                )
                await session.commit()

                resultado = await session.execute(
                    select(EnderecoModel).where(EnderecoModel.id == request.id)
                )
                enderecos_atualizados = resultado.scalars().first()

                return dados_pb2.Endereco(
                    id=enderecos_atualizados.id,
                    rua=enderecos_atualizados.rua,
                    numero=enderecos_atualizados.numero,
                    bairro=enderecos_atualizados.bairro,
                    cidade=enderecos_atualizados.cidade,
                    estado=enderecos_atualizados.estado,
                    cep=enderecos_atualizados.cep
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Endereco()

    async def DeleteEndereco(self, request: dados_pb2.EnderecoRequest, context):
        async with AsyncSessionLocal() as session:
            try:
                #verificando se o endereco existe
                resultado = await session.execute(
                    select(EnderecoModel).where(EnderecoModel.id == request.id)
                )
                endereco_existente = resultado.scalars().first()

                if endereco_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Endereço Indisponível")
                    return dados_pb2.Empty()

                #removendo o endereco
                await session.execute(
                    delete(EnderecoModel).where(EnderecoModel.id == request.id)
                )
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()


class PlataformaService(dados_pb2_grpc.PlataformaServiceServicer):

    async def GetPlataforma(self, request, context):
        async with AsyncSessionLocal() as session:
            #exemplo de consulta assíncrona
            result = await session.execute(
                select(PlataformaModel).where(PlataformaModel.id == request.id)
            )
            item = result.scalars().first()

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
        async with AsyncSessionLocal() as session:
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
        async with AsyncSessionLocal() as session:
            query = select(PlataformaModel)
            if request.HasField('nome'):
                query = select(PlataformaModel).where(PlataformaModel.nome == request.nome)
            if request.HasField('tipo'):
                query = select(PlataformaModel).where(PlataformaModel.tipo == request.tipo)

            resultados = await session.execute(query)
            plataformas = resultados.scalars().all()

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
        async with AsyncSessionLocal() as session:
            try:
                #verificando se a plataforma existe
                resultado = await session.execute(
                    select(PlataformaModel).where(PlataformaModel.id == request.id)
                )
                plataforma_existente = resultado.scalars().first()

                if plataforma_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Plataforma Indisponível")
                    return dados_pb2.Plataforma()
                
                #atualizando a plataforma
                await session.execute(
                    update(PlataformaModel)
                    .where(PlataformaModel.id == request.id)
                    .values(
                        nome=request.nome,
                        email=request.email,
                        website=request.website,
                        tipo=request.tipo
                    )
                )
                await session.commit()

                resultado = await session.execute(
                    select(PlataformaModel).where(PlataformaModel.id == request.id)
                )
                plataforma_atualizadas = resultado.scalars().first()

                return dados_pb2.Plataforma(
                    id=plataforma_atualizadas.id,
                    nome=plataforma_atualizadas.nome,
                    email=plataforma_atualizadas.email,
                    website=plataforma_atualizadas.website,
                    tipo=plataforma_atualizadas.tipo

                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Plataforma()

    async def DeletePlataforma(self, request: dados_pb2.PlataformaRequest, context):
        async with AsyncSessionLocal() as session:
            try:
                #verificando se a plataforma existe
                resultado = await session.execute(
                    select(PlataformaModel).where(PlataformaModel.id == request.id)
                )
                plataforma_existente = resultado.scalars().first()

                if plataforma_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Plataforma Indisponível")
                    return dados_pb2.Empty()

                #removendo a plataforma
                await session.execute(
                    delete(PlataformaModel).where(PlataformaModel.id == request.id)
                )
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()


class ProfessorService(dados_pb2_grpc.ProfessorServiceServicer):

    async def GetProfessor(self, request, context):
        async with AsyncSessionLocal() as session:
            #exemplo de consulta assíncrona
            result = await session.execute(
                select(ProfessorModel).where(ProfessorModel.id == request.id)
            )
            item = result.scalars().first()

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
        async with AsyncSessionLocal() as session:
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
        async with AsyncSessionLocal() as session:
            query = select(ProfessorModel)
            if request.HasField('vertente'):
                query = select(ProfessorModel).where(ProfessorModel.vertente == request.vertente)
            if request.HasField('formacao'):
                query = select(ProfessorModel).where(ProfessorModel.formacao == request.formacao)

            resultados = await session.execute(query)
            professores = resultados.scalars().all()

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
        async with AsyncSessionLocal() as session:
            try:
                #verificando se o professor existe
                resultado = await session.execute(
                    select(ProfessorModel).where(ProfessorModel.id == request.id)
                )
                professor_existente = resultado.scalars().first()

                if professor_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Professor Indisponível")
                    return dados_pb2.Professor()
                
                #atualizando o professor
                await session.execute(
                    update(ProfessorModel)
                    .where(ProfessorModel.id == request.id)
                    .values(
                        nome=request.nome,
                        vertente=request.vertente,
                        telefone=request.telefone,
                        email=request.email,
                        website=request.website,
                        formacao=request.formacao
                    )
                )
                await session.commit()

                resultado = await session.execute(
                    select(ProfessorModel).where(ProfessorModel.id == request.id)
                )
                professor_atualizado = resultado.scalars().first()

                return dados_pb2.Professor(
                    id=professor_atualizado.id,
                    nome=professor_atualizado.nome,
                    vertente=professor_atualizado.vertente,
                    telefone=professor_atualizado.telefone,
                    email=professor_atualizado.email,
                    website=professor_atualizado.website,
                    formacao=professor_atualizado.formacao

                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Professor()

    async def DeleteProfessor(self, request: dados_pb2.ProfessorRequest, context):
        async with AsyncSessionLocal() as session:
            try:
                #verificando se o professor existe
                resultado = await session.execute(
                    select(ProfessorModel).where(ProfessorModel.id == request.id)
                )
                professor_existente = resultado.scalars().first()

                if professor_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Professor Indisponível")
                    return dados_pb2.Empty()

                #removendo a plataforma
                await session.execute(
                    delete(ProfessorModel).where(ProfessorModel.id == request.id)
                )
                await session.commit()

                return dados_pb2.Empty()
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Empty()


class BolsaService(dados_pb2_grpc.BolsaServiceServicer):

    async def GetBolsa(self, request, context):
        async with AsyncSessionLocal() as session:
            #exemplo de consulta assíncrona
            result = await session.execute(
                select(BolsaModel).where(BolsaModel.id == request.id)
            )
            item = result.scalars().first()

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
        async with AsyncSessionLocal() as session:
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
                    data_inicio=novo_item.data_inicio,
                    data_fim=novo_item.data_fim,
                    professor_id=novo_item.professor_id,
                    success=True
                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Bolsa(success=False)

    async def ListBolsas(self, request: dados_pb2.ListBolsasRequest, context):
        async with AsyncSessionLocal() as session:
            query = select(BolsaModel)
            if request.HasField('vertente'):
                query = select(BolsaModel).where(BolsaModel.vertente == request.vertente)
            if request.HasField('remunerado'):
                query = select(BolsaModel).where(BolsaModel.remunerado == request.remunerado)
            if request.HasField('horas_semanais'):
                query = select(BolsaModel).where(BolsaModel.horas_semanais == request.horas_semanais)

            resultados = await session.execute(query)
            bolsas = resultados.scalars().all()

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
        async with AsyncSessionLocal() as session:
            try:
                #verificando se a bolsa existe
                resultado = await session.execute(
                    select(BolsaModel).where(BolsaModel.id == request.id)
                )
                bolsa_existente = resultado.scalars().first()

                if bolsa_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Bolsa Indisponível")
                    return dados_pb2.Bolsa()
                
                #atualizando a bolsa
                await session.execute(
                    update(BolsaModel)
                    .where(BolsaModel.id == request.id)
                    .values(
                        nome=request.nome,
                        vertente=request.vertente,
                        salario=request.salario,
                        remunerado=request.remunerado,
                        horas_semanais=request.horas_semanais,
                        quantidade_vagas=request.quantidade_vagas,
                        descricao=request.descricao,
                        data_inicio=request.data_inicio,
                        data_fim=request.data_fim,
                        professor_id=request.professor_id,
                    )
                )
                await session.commit()

                resultado = await session.execute(
                    select(BolsaModel).where(BolsaModel.id == request.id)
                )
                bolsa_atualizada = resultado.scalars().first()

                return dados_pb2.Bolsa(
                    id=bolsa_atualizada.id,
                    nome=bolsa_atualizada.nome,
                    vertente=bolsa_atualizada.vertente,
                    salario=bolsa_atualizada.salario,
                    remunerado=bolsa_atualizada.remunerado,
                    horas_semanais=bolsa_atualizada.horas_semanais,
                    quantidade_vagas=bolsa_atualizada.quantidade_vagas,
                    descricao=bolsa_atualizada.descricao,
                    data_inicio=bolsa_atualizada.data_inicio,
                    data_fim=bolsa_atualizada.data_fim,
                    professor_id=bolsa_atualizada.professor_id,

                )
            except Exception as e:
                await session.rollback()
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(str(e))
                return dados_pb2.Bolsa()
            
    async def DeleteBolsa(self, request: dados_pb2.BolsaRequest, context):
        async with AsyncSessionLocal() as session:
            try:
                #verificando se o professor existe
                resultado = await session.execute(
                    select(BolsaModel).where(BolsaModel.id == request.id)
                )
                bolsa_existente = resultado.scalars().first()

                if bolsa_existente is None:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("Bolsa Indisponível")
                    return dados_pb2.Empty()

                #removendo a bolsa
                await session.execute(
                    delete(BolsaModel).where(BolsaModel.id == request.id)
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
    #inicializando o banco de dados
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    #configurando o servidor o grpc
    servidor = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    dados_pb2_grpc.add_EnderecoServiceServicer_to_server(EnderecoService(), servidor)
    dados_pb2_grpc.add_PlataformaServiceServicer_to_server(PlataformaService(), servidor)
    dados_pb2_grpc.add_ProfessorServiceServicer_to_server(ProfessorService(), servidor)
    dados_pb2_grpc.add_BolsaServiceServicer_to_server(BolsaService(), servidor)
    servidor.add_insecure_port('[::]:50051')
    await servidor.start()
    print("Servidor inicializou na porta 50051")
    await servidor.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())


# class UserService(dados_pb2_grpc.UserServiceServicer):
#     def CreateUser(self, request, context):
#         conn = get_db_connection()
#         cursor = conn.cursor()
        
#         # Insere o usuário no banco de dados
#         cursor.execute(
#             "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email",
#             (request.name, request.email)
#         )
#         user = cursor.fetchone()
#         conn.commit()
        
#         # Fecha a conexão
#         cursor.close()
#         conn.close()
        
#         return dados_pb2.UserResponse(id=user[0], name=user[1], email=user[2])

#     def GetUser(self, request, context):
#         conn = get_db_connection()
#         cursor = conn.cursor()
        
#         # Busca o usuário pelo id
#         cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (request.name,))
#         user = cursor.fetchone()
        
#         cursor.close()
#         conn.close()
        
#         if user:
#             return dados_pb2.UserResponse(id=user[0], name=user[1], email=user[2])
#         else:
#             context.set_details(f"User with id {request.name} not found.")
#             context.set_code(grpc.StatusCode.NOT_FOUND)
#             return dados_pb2.UserResponse()

# # Configura o servidor gRPC
# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     dados_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
#     server.add_insecure_port('[::]:50051')
#     print("Server is running on port 50051...")
#     server.start()
#     server.wait_for_termination()

# if __name__ == "__main__":
#     serve()

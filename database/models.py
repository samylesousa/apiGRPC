import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
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
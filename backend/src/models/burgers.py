from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from db.database import Base


metadata = Base.metadata

burger_opcionais_table = Table(
    "burger_opcionais",
    Base.metadata,
    Column("burger_id", ForeignKey("burger.id", ondelete="CASCADE")),
    Column("opcional_id", ForeignKey("opcional.id")),
    UniqueConstraint('burger_id', 'opcional_id', name='burguer_opcional_unique'),

)

class Opcional(Base):
    __tablename__ = 'opcional'

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    burgers = relationship('Burger',
        secondary=burger_opcionais_table,
        backref='burger_opcionais', viewonly=True
    )  

class Burger(Base):
    __tablename__ = 'burger'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Numeric(precision=5, scale=2))
    opcionais = relationship(
        "Opcional", secondary=burger_opcionais_table, backref='burger_opcionais', cascade="all, delete", single_parent=True
    )

    carne_id = Column(Integer, ForeignKey("ingrediente.id"))
    pao_id = Column(Integer, ForeignKey("ingrediente.id"))
    status_id = Column(Integer, ForeignKey("status.id"))
    
    carne = relationship("Ingrediente", back_populates="carne_ingrediente", foreign_keys=[carne_id])
    pao = relationship("Ingrediente", back_populates="pao_ingrediente", foreign_keys=[pao_id])

    status = relationship("Status", back_populates='status_burger')


class Ingrediente(Base):
    __tablename__ = 'ingrediente'

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    tipo = Column(String)

    carne_ingrediente = relationship(
        "Burger",
        back_populates="carne",
        foreign_keys=[Burger.carne_id],
    )
    pao_ingrediente = relationship(
        "Burger",
        back_populates="pao",
        foreign_keys=[Burger.pao_id],
    )


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)

    status_burger = relationship("Burger", back_populates='status')
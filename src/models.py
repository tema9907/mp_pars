from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, UniqueConstraint, Double
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from database import Base

Base = declarative_base()
class KTRU(Base):
    __tablename__ = 'ktru'
    id = Column(Integer, primary_key=True,index=True)
    ktru = Column(String)
    name = Column(String)
class right_KTRU(Base):
    __tablename__ = 'right_ktru'
    id = Column(Integer, primary_key=True,index=True)
    ktru = Column(String)
    first_name = Column(String)
    sec_name = Column(String)
#
# class Filter(Base):
#     __tablename__ = 'filters'
#
#     id = Column(UUID(as_uuid=True),nullable=False, primary_key=True, index=True)
#     password = Column(UUID(as_uuid=True), nullable=False)
#     chat_name = Column(String)
#     ktru = Column(String)
#     kato = Column(String)
#     start_price = Column (Integer)
#     end_price = Column (Integer)
#     send_time = Column (String)
#     telegram_chat_ids = Column (String)
#     sended_today = Column (bool)
#     user_id = Column(UUID(as_uuid=True), nullable =False)
#     # delivery_method
#     description = Column(String)
#     start_time = Column (DateTime(timezone=True))
#     end_time = Column (DateTime(timezone=True))

class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(UUID, primary_key=True)
    contract_number = Column(String)  # 111240022111/230054/00  переименовать в contract_number #
    url = Column(String)  # https://goszakup.gov.kz/ru/egzcontract/cpublic/show/18773888' #
    announce_id = Column(String)  # 11004708-1
    contract_type_id = Column(Integer,  ForeignKey('contract_types.id'))  # тут нужно из другой таблички соединить вторичным ключем с контрактом
    status_id = Column(Integer,  ForeignKey('contract_statuses.id'))  # тут тоже нужно соединить с другой табличкой где список статусов
    buying_method_id = Column(Integer,  ForeignKey('contract_purchase_methods.id'))  # тут тоже из другой таблички в которой списки методов
    date_of_creation = Column(DateTime(timezone=True))  # 2023-11-13 15:55:53
    sum = Column(Float)  # 9600000.00
    customer = Column(String)  # ГУ «Отдел строительства
    seller = Column(String)  # МОЛДАБАЕВА РАЙСА'
    customer_name_kz = Column(String)  # «Қаратал ауданының құрылыс, сәулет және қала құрылысы бөлімі» мемлекеттік мекемесі'
    customer_name_ru = Column(String)  # Государственное учреждение «Отдел строител
    customer_BIN = Column(String)  # 111240022111
    customer_RNN = Column(String)  # 091600212569
    seller_name_kz = Column(String)  # 'МОЛДАБАЕВА РАЙСА
    seller_name_ru = Column(String)  # МОЛДАБАЕВА РАЙСА
    seller_BIN = Column(String)  # Нет данных
    seller_IIN = Column(String)  # 560629401367
    seller_RNN = Column(String)  # Нет данных'
    seller_nds = Column(String)  # Без учета НДС'
    fiscal_year = Column(String)  # 2023

    # contract_type_key = relationship('ContractTypeId', foreign_keys=[contract_type_id])
    # status_id_key = relationship('ContractStatuses', foreign_keys=[status_id])
    # buying_method_id_key = relationship('PurchaseMethodsContractId', foreign_keys=[buying_method_id])


class ContractsLot(Base):
    __tablename__ = 'contract_lots'

    id = Column(UUID, primary_key=True)
    contract_id = Column(UUID,  ForeignKey('contracts.id'))
    txt_id = Column(String)  # 43728387 вот с этой странички https://goszakup.gov.kz/ru/egzcontract/cpublic/units/18775632
    number = Column(String)  # 62923074
    url = Column(String)  # 'https://goszakup.gov.kz/ru/registry/show_plan/
    KTRU = Column(String)  # '410010.100.000004'
    name = Column(String)  # Пәтер / Квартира
    quantity = Column(Double)  # 1
    UM = Column(String)  # Единица
    UP = Column(Double)  # 9600000.00
    sum = Column(Double)  # '9600000.00'

    # contract_id_key = relationship('Contract', foreign_keys=[contract_id])



class Announce(Base):
    __tablename__ = 'announces'

    id = Column(UUID(as_uuid=True), nullable=False, primary_key=True, index=True, server_default='gen_random_uuid()')
    announce_number = Column(String, default=None, unique=True)  # 11014031-1 +
    name = Column(String, default=None)  # Услуги полиграфические по изготовлению/печатанию полиграфической продукции (кроме книг, фото, периодических изданий)+
    status_id = Column(String, default=None)  # Опубликовано (прием ценовых предложений)
    type_id = Column(String, default=None)  # 1 из таблицы announsetypes
    item_type_id = Column(String, default=None)  # 1 iz ItemTypes
    purchase_method_id = Column(String, default=None)  # 1 из puchkase_method+
    date_of_creation = Column(DateTime(timezone=True), default=None)  # 2023-11-14 15:11:36
    offers_start_date = Column(DateTime(timezone=True), default=None)  # '2023-11-14 15:14:14+
    offers_end_date = Column(DateTime(timezone=True), default=None)  # 2023-11-21 15:15:20'+
    organizer = Column(String, default=None)  # 060240010094 Коммунальное государственное учреждение "Отдел внутренней политики акимата Сарысуского района"'
    legal_address = Column(String, default=None)  # 316020100, 080700, Казахстан, г. г.Жанатас, ул. Микрорайон 1, д. 18, оф.'
    lots_quantity = Column(Integer, default=None)  # 1
    sum_value = Column(Float, default=None)  # 600 000.00+
    organizer_name_surname = Column(String, default=None)  # АЛТЫНБЕКОВА ГУЛЬНУР ПЕРНЕБЕКОВНА'
    organizer_position = Column(String, default=None)  # Руководитель отдела
    organizer_phone = Column(String, default=None)  # 'Нет данных'
    organizer_email = Column(String, default=None)  # ovp_sarysu@mail.kz
    announce_creator = Column(String, default=None)  # Нет данных'
    url = Column(String, default=None)  # https://goszakup.gov.kz/ru/announce/index/11014031+
    open_start_date = Column(DateTime(timezone=True), default=None)  # None,
    open_end_date = Column(DateTime(timezone=True), default=None)  # None
    platform = Column(String, default=None)

    # status_id_key = relationship('AnnouncesStatuses', foreign_keys=[status_id])
    # type_id_key = relationship('AnnouncesTypes', foreign_keys=[type_id])
    # item_type_id_key = relationship('ItemTypes', foreign_keys=[item_type_id])
    # purchase_method_id_key = relationship('PurchaseMethods', foreign_keys=[purchase_method_id])

    __table_args__ = (UniqueConstraint('status_id', 'announce_number', name='announces_announce_number_status_id_uindex'),)





class Lot_announce(Base):
    __tablename__ = 'lot_announces'

    id = Column(UUID, primary_key=True, index=True, server_default='gen_random_uuid()')
    announce_id = Column(UUID,  ForeignKey('announces.id'))  # ВТОРИЧНЫЙ КЛЮЧ
    ktru_code = Column(String, default=None)
    ktru_name = Column(String, default=None)
    kato = Column(String, default=None)
    delivery_location = Column(String, default=None)
    spec_url = Column(String, default=None)
    quantity = Column(Float, default=None)
    brief_characteristics = Column(String, default=None)
    additional_characteristics = Column(String, default=None)
    funding_source = Column(String, default=None)
    unit_price = Column(Float, default=None)
    unit_measurement_id = Column(String, default=None)
    year1_amount = Column(Float, default=None)
    year2_amount = Column(Float, default=None)
    year3_amount = Column(Float, default=None)
    planned_amount = Column(Float, default=None)
    advance_payment_percentage = Column(String, default=None)
    tru_delivery_period = Column(String, default=None)
    incoterms = Column(String, default=None)
    engineering_service = Column(String, default=None)
    dumping_attribute = Column(String, default=None)
    dumping_calculation_amount = Column(String, default=None)
    organizer_name = Column(String, default=None)
    organizer_bin = Column(String, default=None)
    organizer_position = Column(String, default=None)
    organizer_contact_phone = Column(String, default=None)
    organizer_email = Column(String, default=None)
    organizer_bank_details = Column(String, default=None)
    sended_to = Column(String, default=None)
    lot_number = Column(String, default=None)
    announce_number = Column(String, default=None)
    platform = Column(String, default=None)

    # announce_id_key = relationship('Announce', foreign_keys=[announce_id])

class Ktru_name(Base):
    __tablename__ = "ktru_name"

    id = Column(UUID, primary_key=True,index=True, server_default='gen_random_uuid()')
    ktru = Column(String, default=None)
    name = Column(String, default=None)
    platform = Column(String, default=None)
    company_type= Column(String, default=None)
    category = Column(String, default=None)
# class KTRU(Base):
#     __tablename__ = "ktru"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     ktru_value = Column(String(50), index=True, unique=True)
#     ktru_name = Column(String(400))


class KATO(Base):
    __tablename__ = "kato"

    id = Column(Integer, primary_key=True, autoincrement=True)
    kato_value = Column(String(15))
    region = Column(String(400))
    region_parent = Column(String(400))


# Announce.metadata.create_all(engine)
# Lot.metadata.create_all(engine)
# KTRU.metadata.create_all(engine)
# KATO.metadata.create_all(engine)
# Contract.metadata.create_all(engine)
# ContractsLot.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
#
# all_records = session.query(Announce).all()
# for record in all_records:
#     print(record.__dict__)



class ContractStatuses(Base):
    __tablename__ = 'contract_statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class ContractTypeId(Base):
    __tablename__ = 'contract_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class PurchaseMethodsContractId(Base):
    __tablename__ = 'contract_purchase_methods'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class AnnouncesTypes(Base):
    __tablename__ = 'announce_types'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 1
    name = Column(String)  # Первая закупка


class PurchaseMethods(Base):
    __tablename__ = 'purchase_methods'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 1
    name = Column(String)  # Запрос ценовых предложе


class ItemTypes(Base):
    __tablename__ = 'item_types'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 1
    name = Column(String)  # Услуга


class AnnouncesStatuses(Base):
    __tablename__ = 'announce_statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Filter(Base):
    __tablename__ = "filters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(UUID(as_uuid=True), default=uuid.uuid4)
    chat_name = Column(String, nullable=True)
    ktru = Column(String, nullable=True)
    kato = Column(String, nullable=True)
    start_price = Column(Integer, nullable=True)
    end_price = Column(Integer, nullable=True)
    send_time = Column(String, nullable=True)
    telegram_chat_ids = Column(String, nullable=True)
    sended_today = Column(Boolean, nullable=True)
    # days string[]

class FilteredLots(Base):
    __tablename__ = "filtered_lots"

    id = Column(UUID, primary_key=True)
    filter_id = Column(UUID, ForeignKey('filters.id'), nullable=False)
    announce_id = Column(UUID, ForeignKey('announces.id'))
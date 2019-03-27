import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, Enum, DateTime
from sqlalchemy.orm import relationship
from flask_appbuilder import Model, SQLA



class Model1(Model):
    id = Column(Integer, primary_key=True)
    field_string = Column(String(50), unique=True, nullable=False)
    field_integer = Column(Integer())
    field_float = Column(Float())
    field_date = Column(Date())

    def __repr__(self):
        return str(self.field_string)

    def full_concat(self):
        return "{}.{}.{}.{}".format(
            self.field_string,
            self.field_integer,
            self.field_float,
            self.field_date
        )


class Model2(Model):
    id = Column(Integer, primary_key=True)
    field_string = Column(String(50), unique=True, nullable=False)
    field_integer = Column(Integer())
    field_float = Column(Float())
    field_date = Column(Date())
    excluded_string = Column(String(50), default='EXCLUDED')
    default_string = Column(String(50), default='DEFAULT')
    group_id = Column(Integer, ForeignKey('model1.id'), nullable=False)
    group = relationship("Model1")

    def __repr__(self):
        return str(self.field_string)

    def field_method(self):
        return "field_method_value"


class Model3(Model):
    pk1 = Column(Integer(), primary_key=True)
    pk2 = Column(DateTime(), primary_key=True)
    field_string = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return str(self.field_string)


class TmpEnum(enum.Enum):
    e1 = 'one'
    e2 = 'two'


class ModelWithEnums(Model):
    id = Column(Integer, primary_key=True)
    enum1 = Column(Enum(TmpEnum), info={'enum_class': TmpEnum})


    """ ---------------------------------
            TEST HELPER FUNCTIONS
        ---------------------------------
    """


def insert_data(session, count):
    model1_collection = list()
    for i in range(count):
        model = Model1()
        model.field_string = "test{}".format(i)
        model.field_integer = i
        model.field_float = float(i)
        session.add(model)
        session.commit()
        model1_collection.append(model)
    for i in range(count):
        model = Model2()
        model.field_string = "test{}".format(i)
        model.field_integer = i
        model.field_float = float(i)
        model.group = model1_collection[i]
        session.add(model)
        session.commit()
    for i in range(count):
        model = ModelWithEnums()
        model.enum1 = 'e1'
        model.enum2 = TmpEnum.e2
        session.add(model)
        session.commit()

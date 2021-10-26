from sqlalchemy import create_engine, Column, String, Sequence
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.exc import IntegrityError

Base = declarative_base()


class VlanDb(Base):
    """
    ORM object/table
    """
    __tablename__ = "vlans"
    id = Column(String(10), Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20))
    description = Column(String(50))

    def __repr__(self):
        return f"<Table(vlan_id={self.id}, vlan_name={self.name}, vlan_description={self.description}>"


class VlanPerDevice(Base):
    """
    ORM object/table
    """
    __tablename__ = "vlans_per_device"
    device = Column(String(10), Sequence('user_id_seq'), primary_key=True)
    id = Column(String(10))
    name = Column(String(20))
    description = Column(String(50))

    def __repr__(self):
        return f"<Table(Device={self.device}, vlan_id={self.id}, vlan_name={self.name}, vlan_description={self.description}>"


def add_vlan(session_obj, logger_orm, vlan_id, vlan_name, vlan_description="change_me"):
    """
    Add a VLAN to the DB
    """
    session = session_obj()
    vlan = VlanDb(id=vlan_id, name=vlan_name, description=vlan_description)
    session.add(vlan)
    try:
        session.commit()
    except IntegrityError:
        logger_orm.debug(f"ADD VLAN {vlan_id} {vlan_name} {vlan_description} CAN NOT ADD ALREADY EXISTS")
    else:

        logger_orm.info(f"ADD VLAN {vlan_id} {vlan_name} {vlan_description} ADDED")


def delete_vlan(session_obj, logger_orm, vlan_id):
    """
    Delete a VLAN from the DB
    """
    session = session_obj()
    vlan = session.query(VlanDb).filter_by(id=vlan_id).first()
    try:
        session.delete(vlan)
    except UnmappedInstanceError:
        logger_orm.debug(f"DELETE VLAN {vlan_id} CAN NOT DELETE")
    else:
        session.flush()
        logger_orm.info(f"DELETE VLAN {vlan.id} {vlan.name} {vlan.description} DELETED")


def update_vlan(session_obj, logger_orm, vlan_id, vlan_name, vlan_description="change_me"):
    """
    Update VLAN record in the DB
    """
    session = session_obj()
    vlan = session.query(VlanDb).filter_by(id=vlan_id).first()
    if vlan is not None:
        vlan.id = vlan_id
        vlan.name = vlan_name
        vlan.description = vlan_description
        session.commit()
        logger_orm.info(f"UPDATE VLAN {vlan} UPDATED ")
    else:
        logger_orm.debug(f"UPDATE VLAN {vlan_id} UPDATE VLAN NOT FOUND")


def query_vlan(session_obj, logger_orm, vlan_id):
    """
    Query for one specific VLAN in the DB
    """
    session = session_obj()
    vlan = session.query(VlanDb).filter_by(id=vlan_id).first()
    if vlan:
        logger_orm.debug(f"QUERY VLAN {vlan.id} {vlan.name} {vlan.description} FOUND")
    else:
        logger_orm.debug(f"QUERY VLAN {vlan_id} NOT FOUND")
    return vlan


def query_all_vlan(session_obj, logger_orm):
    """
    Query all the VLANs in the DB
    """
    session = session_obj()
    vlans = session.query(VlanDb).all()
    if len(vlans) == 0:
        logger_orm.info(f"Database empty")
    else:
        logger_orm.info(f"Database loaded. {len(vlans)} records")
        logger_orm.debug(f"{vlans}")
    return vlans


def init_db():
    """
    Start SQLite DB in memory for testing the tool
    """
    vlan_table = VlanDb()
    device_table = VlanPerDevice()
    engine = create_engine('sqlite:///vlan_sync.sqlite', echo=True, logging_name="orm")
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)
    session_obj = scoped_session(session_factory)
    return session_obj


# Session = init_db()
# add_vlan("1", "user")
# query_all_vlan(Session)
# add_vlan("1", "user")
# query_vlan("1")
# update_vlan("1", "pepe")
# update_vlan("2", "pepe")
# query_vlan("1")
# delete_vlan("1")
# delete_vlan("1")
# query_vlan("1")


# vlans_device = [{'vlan_id': '1', 'vlan_name': 'default'}, {'vlan_id': '110', 'vlan_name': 'vlan'},
#                 {'vlan_id': '200', 'vlan_name': 'INET_DTV'}, {'vlan_id': '201', 'vlan_name': 'para_borrar'},
#                 {'vlan_id': '202', 'vlan_name': 'Internet_Broadband'},
#                 {'vlan_id': '251', 'vlan_name': 'InsideFW_REGION(172.21.0.160/29)'},
#                 {'vlan_id': '280', 'vlan_name': 'INSIDE_CONC_VPN(172.21.1.0/28)'},
#                 {'vlan_id': '302', 'vlan_name': 'MPLS-IN'}, {'vlan_id': '303', 'vlan_name': 'descri'},
#                 {'vlan_id': '304', 'vlan_name': 'OutLevel3(201.234.41.80/28)'},
#                 {'vlan_id': '308', 'vlan_name': 'WIFI-PROV-OUT'},
#                 {'vlan_id': '400', 'vlan_name': 'MGMT(172.21.31.32/29)'},
#                 {'vlan_id': '401', 'vlan_name': 'WLC-MGMT(172.21.31.0/29)'},
#                 {'vlan_id': '402', 'vlan_name': 'ARG2FW(172.21.31.16/29)'},
#                 {'vlan_id': '404', 'vlan_name': 'WLC-corp(172.21.92.0/22)'},
#                 {'vlan_id': '405', 'vlan_name': 'WLC-Guest'}, {'vlan_id': '406', 'vlan_name': 'WIFI-Prov'},
#                 {'vlan_id': '407', 'vlan_name': 'ISE(172.21.31.40/29)'}, {'vlan_id': '408', 'vlan_name': 'WLC-HA'},
#                 {'vlan_id': '440', 'vlan_name': 'Failover-FW-AR-MTZ-FW-01-Guest'},
#                 {'vlan_id': '441', 'vlan_name': 'Failover-FW-AR-MTZ-VC-01'},
#                 {'vlan_id': '442', 'vlan_name': 'Failover-FW-AR-MTZ-CO-01'},
#                 {'vlan_id': '443', 'vlan_name': 'Failover-FW-AR-MTZ-FW-01-Prov'},
#                 {'vlan_id': '445', 'vlan_name': 'Failover-Fw-DTV-FW-DC-C-1'},
#                 {'vlan_id': '950', 'vlan_name': 'BC-AFM(172.21.1.16/28)'}, {'vlan_id': '999', 'vlan_name': 'dump-vlan'},
#                 {'vlan_id': '1002', 'vlan_name': 'fddi-default'},
#                 {'vlan_id': '1003', 'vlan_name': 'token-ring-default'},
#                 {'vlan_id': '1004', 'vlan_name': 'fddinet-default'}, {'vlan_id': '1005', 'vlan_name': 'trnet-default'},
#                 {'vlan_id': '1', 'vlan_name': 'enet'}, {'vlan_id': '110', 'vlan_name': 'enet'},
#                 {'vlan_id': '200', 'vlan_name': 'enet'}, {'vlan_id': '201', 'vlan_name': 'enet'},
#                 {'vlan_id': '202', 'vlan_name': 'enet'}, {'vlan_id': '251', 'vlan_name': 'enet'},
#                 {'vlan_id': '280', 'vlan_name': 'enet'}, {'vlan_id': '302', 'vlan_name': 'enet'},
#                 {'vlan_id': '303', 'vlan_name': 'enet'}, {'vlan_id': '304', 'vlan_name': 'enet'},
#                 {'vlan_id': '308', 'vlan_name': 'enet'}, {'vlan_id': '400', 'vlan_name': 'enet'},
#                 {'vlan_id': '401', 'vlan_name': 'enet'}, {'vlan_id': '402', 'vlan_name': 'enet'},
#                 {'vlan_id': '404', 'vlan_name': 'enet'}, {'vlan_id': '405', 'vlan_name': 'enet'},
#                 {'vlan_id': '406', 'vlan_name': 'enet'}, {'vlan_id': '407', 'vlan_name': 'enet'},
#                 {'vlan_id': '408', 'vlan_name': 'enet'}, {'vlan_id': '440', 'vlan_name': 'enet'},
#                 {'vlan_id': '441', 'vlan_name': 'enet'}, {'vlan_id': '442', 'vlan_name': 'enet'},
#                 {'vlan_id': '443', 'vlan_name': 'enet'}, {'vlan_id': '445', 'vlan_name': 'enet'},
#                 {'vlan_id': '950', 'vlan_name': 'enet'}, {'vlan_id': '999', 'vlan_name': 'enet'},
#                 {'vlan_id': '1002', 'vlan_name': 'fddi'}, {'vlan_id': '1003', 'vlan_name': 'tr'},
#                 {'vlan_id': '1004', 'vlan_name': 'fdnet'}, {'vlan_id': '1005', 'vlan_name': 'trnet'}]

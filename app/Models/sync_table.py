from sqlalchemy import Column,String,DateTime
from app.Database.database import Base


class SyncTable(Base):

    __tablename__="sync_state"

    pipeline_name= Column(String(50),nullable=False,primary_key=True)
    last_sync_time=Column(DateTime)
    updated_at=Column(DateTime)

    def __repr__(self):
            return f"<SyncTable(pipeline_name={self.pipeline_name}, last_sync={self.last_sync_time})>"
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declared_attr, relationship
from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
from typing import Any, Dict
from ..config import settings
import asyncio

DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    hash = Column(String, unique=True, nullable=False)
    from_addr = Column(String)
    to_addr = Column(String)
    value = Column(String)
    gas = Column(String)
    input = Column(String, nullable=True)
    timestamp = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True, index=True)
    tx_id = Column(Integer)
    score = Column(Float)
    features = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def save_transaction(tx: Dict[str, Any]) -> int:
    async with AsyncSessionLocal() as session:
        db_tx = Transaction(
            hash=tx.get('hash'),
            from_addr=tx.get('from_addr') or tx.get('from'),
            to_addr=tx.get('to_addr') or tx.get('to'),
            value=str(tx.get('value')),
            gas=str(tx.get('gas')),
            input=tx.get('input'),
            timestamp=tx.get('timestamp')
        )
        session.add(db_tx)
        await session.commit()
        await session.refresh(db_tx)
        return db_tx.id

async def save_prediction(tx_id: int, score: float, features: list):
    async with AsyncSessionLocal() as session:
        pred = Prediction(tx_id=tx_id, score=score, features=features)
        session.add(pred)
        await session.commit()
        await session.refresh(pred)
        return pred.id

async def get_metrics():
    async with AsyncSessionLocal() as session:
        tx_count = await session.execute('SELECT COUNT(*) FROM transactions')
        pred_count = await session.execute('SELECT COUNT(*) FROM predictions')
        # The result of execute of raw SQL is driver-dependent; use fallback queries
        tx_count_val = (await session.scalar('SELECT COUNT(*) FROM transactions'))
        pred_count_val = (await session.scalar('SELECT COUNT(*) FROM predictions'))
        return {'transactions': int(tx_count_val or 0), 'predictions': int(pred_count_val or 0)}

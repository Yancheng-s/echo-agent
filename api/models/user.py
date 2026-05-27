from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

SCHEMA = "account"


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(f"{SCHEMA}.users.id"), unique=True, nullable=False)
    display_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    language = Column(String, default="zh-CN")
    timezone = Column(String, default="Asia/Shanghai")
    theme = Column(String, default="dark")


class UserUsage(Base):
    __tablename__ = "user_usage"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(f"{SCHEMA}.users.id"), unique=True, nullable=False)
    total_queries = Column(Integer, default=0)
    daily_queries = Column(Integer, default=0)
    daily_limit = Column(Integer, default=50)
    reset_at = Column(DateTime, nullable=True)

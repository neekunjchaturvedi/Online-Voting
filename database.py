import os
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)  # Will store hashed password
    votes = relationship("Vote", back_populates="user")

class Candidate(Base):
    __tablename__ = 'candidates'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    votes_received = relationship("Vote", back_populates="candidate")
    
    @property
    def vote_count(self):
        return len(self.votes_received)

class Vote(Base):
    __tablename__ = 'votes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    
    user = relationship("User", back_populates="votes")
    candidate = relationship("Candidate", back_populates="votes_received")

# Create database connection
def get_database_session():
    # Create database if it doesn't exist
    if not os.path.exists('voting_system.db'):
        engine = create_engine('sqlite:///voting_system.db')
        Base.metadata.create_all(engine)
        
        # Create session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Add some default candidates
        default_candidates = [
            Candidate(name="Candidate A", description="Description for Candidate A"),
            Candidate(name="Candidate B", description="Description for Candidate B"),
            Candidate(name="Candidate C", description="Description for Candidate C"),
            Candidate(name="Candidate D", description="Description for Candidate D"),
        ]
        
        session.add_all(default_candidates)
        session.commit()
        return session
    else:
        engine = create_engine('sqlite:///voting_system.db')
        Session = sessionmaker(bind=engine)
        return Session()
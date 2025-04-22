from database import User, Candidate, Vote, get_database_session

def get_all_candidates():
    """Get all candidates from the database"""
    session = get_database_session()
    candidates = session.query(Candidate).all()
    session.close()
    return candidates

def cast_vote(user_id, candidate_id):
    """Cast a vote for a candidate"""
    session = get_database_session()
    
    # Check if user has already voted
    existing_vote = session.query(Vote).filter_by(user_id=user_id).first()
    if existing_vote:
        # Update the vote
        existing_vote.candidate_id = candidate_id
        session.commit()
        session.close()
        return True, "Vote updated successfully"
    
    # Create new vote
    new_vote = Vote(user_id=user_id, candidate_id=candidate_id)
    session.add(new_vote)
    session.commit()
    session.close()
    
    return True, "Vote cast successfully"

def get_user_vote(user_id):
    """Get the candidate a user voted for"""
    session = get_database_session()
    
    vote = session.query(Vote).filter_by(user_id=user_id).first()
    if not vote:
        session.close()
        return None
    
    candidate = session.query(Candidate).filter_by(id=vote.candidate_id).first()
    session.close()
    
    return candidate

def get_vote_results():
    """Get vote counts for all candidates, sorted by votes received"""
    session = get_database_session()
    
    candidates = session.query(Candidate).all()
    
    # Count votes for each candidate
    results = []
    for candidate in candidates:
        vote_count = session.query(Vote).filter_by(candidate_id=candidate.id).count()
        results.append({
            'id': candidate.id,
            'name': candidate.name,
            'description': candidate.description,
            'votes': vote_count
        })
    
    session.close()
    
    # Sort by votes (descending)
    results.sort(key=lambda x: x['votes'], reverse=True)
    
    return results
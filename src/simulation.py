import numpy as np
import pandas as pd

def monte_carlo_simulation(iterations: int, 
                         DemLow: float, DemHigh: float, 
                         RepLow: float, RepHigh: float, 
                         NPALow: float, NPAHigh: float,
                         DemMean: float, DemStd: float, 
                         RepMean: float, RepStd: float, 
                         NPAMean: float, NPAStd: float, 
                         RegDems: int, RegReps: int, RegNPAs: int) -> pd.DataFrame:
    """
    Perform Monte Carlo simulation for election outcomes
    
    Args:
        iterations (int): Number of simulation runs
        ... (document other parameters)
    
    Returns:
        pd.DataFrame: Results of the simulation
    """
    output_labels = [
        'Run #', "Dem Votes", "Dem Voters", 
        "Rep Votes", "Rep Voters", 
        "NPA Votes", "NPA Voters", 
        "% of Votes"
    ]
    
    results = pd.DataFrame(columns=output_labels)
    
    for i in range(iterations):
        # Calculate estimated # of voter share per party
        DemVoterShare = np.floor(np.random.uniform(DemLow, DemHigh+1))/100
        RepVoterShare = np.floor(np.random.uniform(RepLow, RepHigh+1))/100
        NPAVoterShare = np.floor(np.random.uniform(NPALow, NPAHigh+1))/100
        
        # Calculate estimated # of voters per party
        DemVoters = np.floor((np.random.normal(DemMean,DemStd)/100)*RegDems)
        RepVoters = np.floor((np.random.normal(RepMean,RepStd)/100)*RegReps)
        NPAVoters = np.floor((np.random.normal(NPAMean,NPAStd)/100)*RegNPAs)
        
        # Calculate totals per party
        DemVotes = np.max([0, np.floor(DemVoters*DemVoterShare)])
        RepVotes = np.max([0, np.floor(RepVoters*RepVoterShare)])
        NPAVotes = np.max([0, np.floor(NPAVoters*NPAVoterShare)])
        
        # Calculate overall totals
        TotalVotes = DemVotes+RepVotes+NPAVotes
        TotalVoters = DemVoters+RepVoters+NPAVoters
        TotalPercent = (TotalVotes/TotalVoters)*100
        
        # Add values to Results dataframe
        new_row = pd.DataFrame({
            'Run #': [i], 
            'Dem Votes': [DemVotes], 
            'Dem Voters': [DemVoters],
            'Rep Votes': [RepVotes], 
            'Rep Voters': [RepVoters],
            'NPA Votes': [NPAVotes], 
            'NPA Voters': [NPAVoters],
            '% of Votes': [TotalPercent]
        })
        
        results = pd.concat([results, new_row], ignore_index=True)
    
    return results

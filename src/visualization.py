import matplotlib.pyplot as plt
import pandas as pd

def plot_election_results(election_results: pd.DataFrame):
    """
    Create histogram of election outcomes
    
    Args:
        election_results (pd.DataFrame): Simulation results
        
    Returns:
        matplotlib.figure.Figure: Plot figure
    """
    fig = plt.figure(figsize=(8, 6))
    plt.hist(election_results['% of Votes'], bins=10, edgecolor='black')
    plt.title('Election Outcome Probabilities')
    plt.xlabel('Election Vote %')
    plt.ylabel('# of Simulation Outcomes')
    return fig

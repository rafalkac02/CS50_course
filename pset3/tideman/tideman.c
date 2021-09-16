#include <cs50.h>
#include <stdio.h>
#include <string.h>

// max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // populate array of candidates
    candidate_count = argc - 1;

    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);
            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }
        record_preferences(ranks);
        printf("\n");
    }
    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    int win_strength[pair_count];
    pair_count = 0;

    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    return;
}

// sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int swaps;
    pair p_hold[pair_count];

    do
    {
        swaps = 0;
        for (int i = 0; i < pair_count - 1; i++)
        {
            if (pairs[i].winner - pairs[i].loser > pairs[i + 1].winner - pairs[i + 1].loser)
            {
                p_hold[i] = pairs[i];
                pairs[i] = pairs[i + 1];
                pairs[i + 1] = p_hold[i];
                swaps++;
            }
        }
    }
    while (swaps != 0);

    // check if pairs are in decreasing order of win_strength
    for (int i = 0; i < pair_count; i++)
    {
        printf("pair %i, pairs[i].winner %i\n", i, pairs[i].winner);
    }
    return;
}

bool cycle(int original_winner, int L)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[i][original_winner])
        {
            if (i != L)
            {
                return cycle(i, L);
            }
            else
            {
                return true;
            }
        }
    }
    return false;
}

// lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0 ; i < pair_count; i++)
    {
        if (cycle(pairs[i].winner, pairs[i].loser) == false)
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
}

// print the winner of the election
void print_winner(void)
{
    for (int b = 0; b < candidate_count; b++)
    {
        int m = 0;
        for (int i = 0; i < pair_count; i++)
        {
            if (b == pairs[i].loser)
            {
                m++;
            }
            if ((m == 0) && (i == pair_count - 1))
            {
                printf("%s\n", candidates[b]);
            }
        }
    }
    string winner;
    int n = 0;
    for (int j = 0; j < candidate_count; j++)
    {
        int t = 0;
        for (int x = 0; x < candidate_count; x++)
        {
            if (locked[j][x] == true)
            {
                t++;
            }
        }
        if (t > n)
        {
            n = t;
            winner = candidates[j];
            printf(" %s\n", winner);
        }
    }
    return;
}
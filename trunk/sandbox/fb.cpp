#include <ext/hash_map>
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

using namespace std;

//typedefs
struct Edge
{
    int v1;
    int v2;
    int m;
    long weight;
};

class Graph
{
public:
    ~Graph()
    {
        delete arr;
    }

    Graph(Graph* other, int exceptedIdx)
    {
        this->arr = new int[other->count - 1];
        for (int i = 0; i < exceptedIdx; i++)
        {
            this->arr[i] = other->arr[i];
        }
        for (int i = exceptedIdx + 1; i < other->count; i++)
        {
            this->arr[i - 1] = other->arr[i];
        }
        this->count = other->count - 1;
    }

    Graph(int from, int to)
    {
        for (int i = from; i < to; i++)
        {
            this->arr[i - from] = i;
        }
        this->count = to - from;
    }
    int* arr;
    int count;
};

class GraphInfo;
{
public:
    ~GraphInfo()
    {
        if (requiredEdges)
        {
            delete requiredEdges;
        }
    }
    GraphInfo(bool connected):requiredEdges(NULL), count(0), isConnected(connected) {}
    int[] requiredEdges;
    int count;
    bool isConnected;
};

//global functions
int EdgeCmp(const Edge* e1, const Edge* e2)
{
    return (e1->v1 == e1->v2) ? (e1->v2 < e2->v2) : (e1->v1 < e2->v1);
}

//global variables
vector<Edge*> edges;
long minCost;
Graph* minGraph;
__gnu_cxx::hash_map<const Graph*, const GraphInfo*, hash<const Graph*>, GraphEqual> cache;

int main()
{
    //read from input
    while (!cin.eof())    
    {
        string m;
        string v1;
        string v2;
        long weight;

        cin >> m;
        cin >> v1;
        cin >> v2;
        cin >> weight;
        
        Edge* e = new Edge;
        e->m = atoi(m.c_str() + 1);
        e->v1 = atoi(v1.c_str() + 1);
        e->v2 = atoi(v2.c_str() + 1);
        e->weight = weight;

        edges.push_back(e);
    }
    sort(edges.begin(), edges.end(), EdgeCmp);
    
    //TODO - remove extra edge connect to same points

    //implement a bfs
    //need a catch hash<graph*> -> vector<int> /*sorted required edges*/)
    //graph:
    //int[] all edges(sorted)
    queue<Graph*> q;
    Graph* initG = new Graph(0, edges.size());
    hash[initG] = new 
    while (!q.empty())
    { 
        Graph* graph = q.pop();
        GraphInfo* info = cache(cur);
        bool isMinimum = false;
        vector<int> requiredEdges;
        for (int i = 0; i < graph->count; i++)
        {
            if (!IsRequireEdge(graph->arr[i], info))
            {
                Graph* newGraph = new Graph(graph, graph->arr[i]);
                bool connected = CheckOrAddConnected(newGraph);
                long cost = newGraph->GetCost();
                if (connected)
                {
                    q.push(newGraph); 
                    if (cost < minCost)
                    {
                        minCost = cost;
                        minGraph = newGraph;
                    }
                }
                else
                {
                    requiredEdges.push_back(graph->arr[i]);
                }
            }
        }
        //merge required edges
        //TODO (don't have good idea yet!)
    }
}

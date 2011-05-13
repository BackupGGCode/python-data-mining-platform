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

struct Vertex
{
    int id;
    int lowlink;
    int index;

    Vertex(int _id): id(_id), lowlink(0), index(0) {}
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
    ~GraphInfo() { }
    
    GraphInfo(bool connected): isConnected(connected) {}
    vector<int> requiredEdges;
    bool isConnected;
};

typedef __gnu_cxx::hash_map<const Graph*, const GraphInfo*, hash<const Graph*>, GraphEqual> CacheMap;

//global functions
int EdgeCmp(const Edge* e1, const Edge* e2)
{
    return (e1->v1 == e1->v1) ? (e1->v2 < e2->v2) : (e1->v1 < e2->v1);
}

//global variables
vector<Edge*> edges;
vector<Vertex*> vertice;
long minCost;
Graph* minGraph;
CacheMap cache;
CacheMap::iterator CacheMapIter;

void GetData()
{
    map<int, int> vertexSet;
    int id = 0;
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

        if (vertexSet.find(e->v1) == vertexSet.end())
        {
            vertexSet[id] = e->v1;
            vertice.push_back(new Vertex(e->v1));
        }
        if (vertexSet.find(e->v2) == vertexSet.end())
        {
            vertexSet[id] = e->v2;
            vertice.push_back(new Vertex(e->v2));
        }

        edges.push_back(e);
    }
    sort(edges.begin(), edges.end(), EdgeCmp);
    //TODO - remove extra edge connect to same points
}

void OutputResult()
{
    cout << minCost << endl;
    vector<int> machineList;
    for (int i = 0; i < minGraph->count; i++)
    {
        machineList.push_back(minGraph->arr[i]);
    }
    sort(machineList.begin(), machineList.end());
    for (size_t i = 0; i < machineList.size() - 1; i++)
    {
        cout << machineList[i] << " ";
    }
    cout << machineList[machineList.size() - 1] << endl;
}

bool CheckIsStrongConnected(Graph* graph)
{
    //make a real adjacent graph
    
}

bool CheckOrAddConnected(Graph* graph, GraphInfo** retInfo)
{
    CacheMapIter iter = cache.find(graph);

    //already in map
    if (iter != cache.end())
    {
        *retInfo = iter->second;
        return (*retInfo)->isConnected;
    }
    else
    {
        GraphInfo* info = new GraphInfo;
        info->isConnected = CheckIsStrongConnected(graph);
        cache[graph] = info;
        *retInfo = info;
        return info->isConnected;
    }
}

int main()
{
    //implement a bfs
    //need a catch hash<graph*> -> vector<int> /*sorted required edges*/)
    //graph:
    //int[] all edges(sorted)
    queue<Graph*> q;
    Graph* initG = new Graph(0, edges.size());
    cache[initG] = new GraphInfo;

    //start bfs search
    while (!q.empty())
    { 
        Graph* graph = q.pop();
        GraphInfo* info = cache(graph);
        bool isMinimum = false;
        vector<int> requiredEdges;
        vecotr<GraphInfo*> sonInfos; //for merge required edges

        for (int i = 0; i < graph->count; i++)
        {
            if (!IsRequireEdge(graph->arr[i], info))
            {
                GraphInfo* newInfo = NULL;
                Graph* newGraph = new Graph(graph, graph->arr[i]);
                bool connected = CheckOrAddConnected(newGraph, &newInfo);
                long cost = newGraph->GetCost();
                if (connected)
                {
                    sonInfos.push_back(newInfo);
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
        for (size_t i = 0; i < sonInfos.size(); i++)
        {
            sonInfos[i].requiredEdges = requiredEdges;
        }

        //remove GraphInfo from cache
        delete info;
        cache.erase(graph);
    }

    OutputResult();
}

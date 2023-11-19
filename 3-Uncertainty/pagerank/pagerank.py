import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2: #MUDAR PARA 2
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    # corpus = crawl("corpus0") #APAGAR AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    res = {}

    keys, values = list(corpus.keys()), list(corpus.values())
    page_index = keys.index(page)
    possiveis = list(values[page_index])
    if len(possiveis) == 0:
            for key in keys:
                res[key] = round(1 / len(keys), 5)
    
    else:


        chance_links = damping_factor / len(possiveis)
        chance_rand = round((1-damping_factor) / len(keys),5)

        for key in keys:
            if key in possiveis:
                res[key] = round(chance_links + chance_rand, 5)
            else:
                res[key] = chance_rand

    


    # if go_rand(damping_factor):
    #     rand = random.randint(0, len(keys)-1)
    #     while page == rand:
    #         rand = random.randint(0, len(keys)-1)

    #     page = keys.index(keys[rand])
            
    # else:
    #     prox = random.randint(0, len(possiveis)-1)
    #     proxima_pagina = keys.index(possiveis[prox])
    #     page = proxima_pagina

    
    return res

def go_rand(damping_factor):
    rand = random.random()
    return rand >= damping_factor

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    

    
    pagina_atual = random.randint(0,len(corpus)-1)
    keys, values = list(corpus.keys()), list(corpus.values())
    pag = keys[pagina_atual]
    ref = [0]*len(corpus)
    ref[pagina_atual] += 1
    for i in range(n-1):
        tm = transition_model(corpus, pag, damping_factor)
        pag_escolhida = random.choices(list(tm.keys()), list(tm.values()))[0]
        pag = pag_escolhida
        ref[keys.index(pag)] += 1
        #achar a apgina atual
        # chamar a funcao transition model
        #receber um dicionario com a probabilidade de ir em cada pagina
        # possiveis = list(values[pagina_atual])
        
        # if go_rand(damping_factor):
        #     rand = random.randint(0, len(keys)-1)
        #     while pagina_atual == rand:
        #         rand = random.randint(0, len(keys)-1)

        #     pagina_atual = keys.index(keys[rand])
            
        # else:
        #     prox = random.randint(0, len(possiveis)-1)
        #     proxima_pagina = keys.index(possiveis[prox])
        #     pagina_atual = proxima_pagina

    valor_porcentagem = round(100 / n, 5)
    res = {}
    for index, key in enumerate(keys):
        res[key] = round((ref[index] * (valor_porcentagem) ) / 100, 5)

    
    return res


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    res = {}
    base = {}
    d = damping_factor
    keys, values = list(corpus.keys()), list(corpus.values())
    n = len(keys)
    initial_pr = round(1 / len(keys), 5)
    
    for key in keys:
        res[key] = initial_pr
    
    base = res.copy()
    controler = True
    while controler:
        
        for key in keys:
            temp = 0
            pr = ((1 - d) / n)
            for index, other_pages  in enumerate(keys):
                if key != other_pages and key in values[index]:
                    x =  len(values[index])
                    if x == 0:
                        x = len(keys)
                    temp += (res[other_pages] / x)
            test = pr + (d*temp)
            res[key] = round(test, 4)

        bases = list(base.values())
        ress = list(res.values())
        for index, val in enumerate(bases):
            if abs(val - ress[index]) < .001:
                controler = False
        base = res.copy()

    

    return base






if __name__ == "__main__":
    main()

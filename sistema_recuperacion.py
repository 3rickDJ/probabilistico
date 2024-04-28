import pandas as pd
import numpy as np
import re
import process_text
import scrap
import process_script
class SistemaDeRecuperacion:
    def __init__(self) -> None:
        ####### SCRAP
        self.items = scrap.scrap() # da el items.json
        ####### Process Corpus, get corpus_stems and Corpus documents
        self.corpus, self.corpus_stems = process_script.load_items(self.items)
        ######## Process Text
        process_script.main() # da el tf.csv
        ########

        #Cargar la matriz tf-idf
        df = pd.read_csv('tf.csv')
        self.df = df
        N = df.shape[0] # N
        stems = df.columns[1:] #Terminos EXCEPTO el nombre del documento
        self.stems = stems

        #Funcion para determinar si un termino esta presente en un documento
        def is_present(column, number=0):
            return (column > number).sum() #Si la frecuencia es mayor a 0, entonces esta presente

        n_k = df.drop(columns='name').apply(is_present) #Numero de documentos en los que aparece cada termino

        id_k = np.log2(N/n_k) #Aplicamos la funcion para calcular el idf
        self.id_k = id_k
        tf_idf = df[stems].mul(id_k, axis=1) #Multiplicamos la matriz tf por el idf
        self.tf_idf = tf_idf

    def query(self, query='none', k=10):
        #################################################################################################################################
        #Consulta del usuario
        query = re.split(r"[^a-z0-9]+", query) #Tokenizamos la consulta
        query = process_text.ProcessData('query', query) #Procesamos la consulta aplicando stopwords y stems
        #Obtenemos un vector de la consulta
        new_row = {key: [ query.frequency.get(key, 0) ] for key in self.df.columns[1:]}
        new_row['name'] = 'query' #Agregamos el nombre del documento
        new_row = pd.DataFrame(new_row, index=[self.df.index.max() + 1]) #Convertimos el diccionario en un dataframe
        new_row = new_row[self.stems].mul(self.id_k, axis=1) #Multiplicamos la matriz tf por el idf
        query_matrix = pd.concat([self.tf_idf, new_row])
        full_table = pd.merge(self.df['name'], query_matrix, left_index=True, right_index=True)
        new_row['name'] = 'query'
        full_table = pd.concat([full_table, new_row])
        full_table.to_csv('query_matrix.csv')

        ##### use kmeans

        X = full_table.drop(['name'], axis=1).values
        # import pudb; pudb.set_trace()
        centroids, labels =  kmeans(X, k=k, max_iter=999)
        print('centroids:\n', centroids)
        print('labels:\n', labels)
        # import pudb; pudb.set_trace()
        df = concat_data_labels(full_table, labels)
        # get sorted data
        point, label = get_point_label_of_query(df, 'query')
        df_sorted = get_sorted_data(df, label, point)
        df_sorted = df_sorted[ df_sorted['label'] == label ]
        # save results
        df_sorted.to_csv('query_matrix_sorted.csv')
        df.to_csv('query_matrix_labeled.csv')
        ##### get list of urls relationated
        lista = df_sorted['name'].tolist()
        print(lista[1:])
        return lista[1:]

if __name__ == "__main__":
    sistema = SistemaDeRecuperacion()
    # import pudb; pudb.set_trace()
    sistema.query('Rowling')

import pandas as pd
from connexion import get_connection

# Top articles importés
def top_articles_import():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT a.designation_article AS article, COUNT(*) AS nombre
        FROM dum d
        JOIN articles a ON d.id_article = a.id_article
        WHERE d.sens = 'Import'
        GROUP BY a.designation_article
        ORDER BY nombre DESC
        LIMIT 10;
        """

        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Article", "Nombre d'importations"])

        cursor.close()
        conn.close()
        return df

    except Exception as e:
        raise Exception(f"Erreur top_articles_import : {e}")

# Top articles exportés
def top_articles_export():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT a.designation_article AS article, COUNT(*) AS nombre
        FROM dum d
        JOIN articles a ON d.id_article = a.id_article
        WHERE d.sens = 'Export'
        GROUP BY a.designation_article
        ORDER BY nombre DESC
        LIMIT 10;
        """

        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Article", "Nombre d'exportations"])

        cursor.close()
        conn.close()
        return df

    except Exception as e:
        raise Exception(f"Erreur top_articles_export : {e}")

# Top pays d'importation
def top_pays_import():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT p.nom_pays AS pays, COUNT(*) AS nombre
        FROM dum d
        JOIN pays p ON d.code_pays = p.code_pays
        WHERE d.sens = 'Import'
        GROUP BY p.nom_pays
        ORDER BY nombre DESC
        LIMIT 10;
        """

        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Pays", "Nombre d'importations"])

        cursor.close()
        conn.close()
        return df

    except Exception as e:
        raise Exception(f"Erreur top_pays_import : {e}")

# Top pays d'export
def top_pays_export():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT p.nom_pays AS pays, COUNT(*) AS nombre
        FROM dum d
        JOIN pays p ON d.code_pays = p.code_pays
        WHERE d.sens = 'Export'
        GROUP BY p.nom_pays
        ORDER BY nombre DESC
        LIMIT 10;
        """

        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Pays", "Nombre d'exportations"])

        cursor.close()
        conn.close()
        return df

    except Exception as e:
        raise Exception(f"Erreur top_pays_export : {e}")
import pandas as pd
from connexion import get_connection



#top pays par valeur monétaire 

def top_valeur_monétaire_par_pays():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT p.nom_pays AS pays, d.sens, SUM(d.valeur_article) AS total_valeur_monétaire
        FROM dum d
        JOIN pays p ON d.code_pays = p.code_pays
        GROUP BY p.nom_pays, d.sens
        ORDER BY total_valeur_monétaire  DESC
        LIMIT 10;
        """

        cursor.execute(query)
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=["Pays", "Sens", "Valeur totale monétaire"])

        cursor.close()
        conn.close()
        return df

    except Exception as e:
        raise Exception(f"Erreur top_valeur_par_pays : {e}")
    

import streamlit as st
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid
from datetime import datetime
import json


CONTACT_POINTS = ['127.0.0.1']
PORT = 9042
KEYSPACE = "crisp_dm_project"

class CassandraManager:
    def __init__(self):
        self.session = None
        self.cluster = None
        self._connect()

    def _connect(self):
        try:
            self.cluster = Cluster(contact_points=CONTACT_POINTS, port=PORT)
            self.session = self.cluster.connect()
            self._initialize_schema()
        except Exception as e:
            st.error(f"Error conectando a Cassandra: {e}")
            st.warning("Asegúrate de que el contenedor Docker esté corriendo: 'sudo docker start cassandra-container'")

    def _initialize_schema(self):
        """Crea el Keyspace y la tabla de metadatos si no existen."""
        if not self.session:
            return

        self.session.execute(f"""
            CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
            WITH REPLICATION = {{ 'class' : 'SimpleStrategy', 'replication_factor' : 1 }}
        """)

        self.session.set_keyspace(KEYSPACE)


        self.session.execute("""
            CREATE TABLE IF NOT EXISTS registro_fases (
                id uuid PRIMARY KEY,
                fase text,
                timestamp timestamp,
                detalles text,
                usuario text
            )
        """)

    def registrar_metadata(self, fase, detalles_dict):
        """Inserta un registro en Cassandra sobre la fase actual."""
        if not self.session:
            return

        query = """
            INSERT INTO registro_fases (id, fase, timestamp, detalles, usuario)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            detalles_json = json.dumps(detalles_dict, default=str)
            self.session.execute(query, (
                uuid.uuid4(),
                fase,
                datetime.now(),
                detalles_json,
                "Eduardo Mendieta"
            ))
            print(f"✅ Metadata registrada en Cassandra para fase: {fase}")
        except Exception as e:
            st.error(f"Error guardando metadata en Cassandra: {e}")

    def obtener_historial(self):
        """Recupera todos los registros para el dashboard novedoso."""
        if not self.session:
            return []
        try:
            rows = self.session.execute("SELECT fase, timestamp, detalles FROM registro_fases")
            return list(rows)
        except Exception as e:
            st.error(f"Error leyendo historial: {e}")
            return []

    def close(self):
        if self.cluster:
            self.cluster.shutdown()


db_manager = CassandraManager()
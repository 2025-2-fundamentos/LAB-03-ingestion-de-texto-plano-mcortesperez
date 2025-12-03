"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
import re
import pandas as pd

def pregunta_01():
  
  """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
  
  with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
      lines = [ln.rstrip() for ln in f.readlines()]

  entries = []
  current = ""

  for ln in lines:
      if re.match(r'^\s*\d+\s+', ln):
          if current:
              entries.append(current)
          current = ln
      elif current and ln.strip():
          current += " " + ln.strip()

  if current:
      entries.append(current)

  rows = []

  for e in entries:
      m = re.match(r'^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$', e)
      if m:
          clu = int(m.group(1))
          cnt = int(m.group(2))
          pct = float(m.group(3).replace(',', '.'))
          rest = m.group(4)
      else:
          nums = re.findall(r'(\d+)', e)
          if len(nums) >= 3:
              clu = int(nums[0])
              cnt = int(nums[1])
              pct = float(nums[2].replace(',', '.'))
              rest = re.split(r'\d+\s*%\s*', e, maxsplit=1)[-1]
          else:
              continue

      rest = rest.strip()
      if rest.endswith('.'):
          rest = rest[:-1]
      rest = re.sub(r'\s+', ' ', rest)

      parts = [p.strip() for p in re.split(r',\s*', rest) if p.strip()]
      kw = ', '.join(parts)

      rows.append((clu, cnt, pct, kw))

  df = pd.DataFrame(
      rows,
      columns=[
          "cluster",
          "cantidad_de_palabras_clave",
          "porcentaje_de_palabras_clave",
          "principales_palabras_clave",
      ],
  )

  df = df.sort_values("cluster").reset_index(drop=True)
  return df
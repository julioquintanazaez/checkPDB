#Imports here
import os
import sys
from collections import Counter

class CheckPDB:

   def __init__(self, excelUrl, pdbUrl, show_results=False):
      self.excel_pdb_url = excelUrl
      self.graph_pdb_url = pdbUrl
      self.pdb_excel_atoms_data = []
      self.pdb_graph_atoms_data = [] 
      self.pdb_excel_concexion_data = []
      self.pdb_graph_concexion_data = [] 
      self.show_results = show_results

   def get_index_from_atoms(self):
      id_atoms_excel = [x[0] for x in self.pdb_excel_atoms_data]
      id_atoms_graph = [x[0] for x in self.pdb_graph_atoms_data]   
      return id_atoms_excel, id_atoms_graph

   def read_atoms(self, url):
      print("Proccessing file to extract Atoms.....")
      data  = []
      try:
         # Using readline()
         file1 = open(url, 'r')
         while True:
            # Get next line from file
            line = file1.readline()
            if not line: # if line is empty
               break
            if not line.startswith("ATOM"):
               continue            
            temp_ = " ".join(line.split()) #remove extra white spaces
            temp_values = temp_.split(" ") #ATOM 1640 N ALA A 1 -453 -433 9 1.00 0.00 N
            tuple_ = (temp_values[1], temp_values[6], temp_values[7], temp_values[8])
            data.append(tuple_)
         return data
      except IOError as e:
         print(e)
         raise ValueError(f"An error occurred during file parsing: {e}.")

   def read_conexion(self, url):
      print("Proccessing file to extract CONECT.....")
      data  = []
      try:
         # Using readline()
         file1 = open(url, 'r')
         while True:
            # Get next line from file
            line = file1.readline()
            if not line: # if line is empty
               break
            if not line.startswith("CONECT"):
               continue            
            temp_ = " ".join(line.split()) #remove extra white spaces
            temp_values = temp_.split(" ") #CONECT 1626 490 0 0
            tuple_ = (temp_values[1], temp_values[2])
            data.append(tuple_)
         return data
      except IOError as e:
         print(e)
         raise ValueError(f"An error occurred during file parsing: {e}.")

   def read_atoms_files(self):
      self.pdb_excel_atoms_data = self.read_atoms(self.excel_pdb_url)
      self.pdb_graph_atoms_data = self.read_atoms(self.graph_pdb_url)
      print("Reading ATOMs files ends")

   def read_conexion_files(self):
      self.pdb_excel_concexion_data = self.read_conexion(self.excel_pdb_url)
      self.pdb_graph_concexion_data = self.read_conexion(self.graph_pdb_url)
      print("Reading CONECT files ends")

   def check_atoms_list_sizes(self):  
      len_pdb_excel = len(self.pdb_excel_atoms_data) 
      len_pdb_graph = len(self.pdb_graph_atoms_data)
      if len_pdb_excel == len_pdb_graph:
         print(f"The ATOMs list have the same sizes: {len_pdb_excel}")
         return True      
      print(f"The ATOMs list haven`t the same sizes, PDBs from Excel {len_pdb_excel} and from Graph {len_pdb_graph}")
      return False   
      
   def check_conect_list_sizes(self):  
      len_pdb_excel = len(self.pdb_excel_concexion_data)
      len_pdb_graph = len(self.pdb_graph_concexion_data)
      if len_pdb_excel == len_pdb_graph:
         print(f"The CONECT list have the same sizes: {len_pdb_excel}")         
      print(f"The CONECT list haven`t the same sizes, PDB from Excel {len_pdb_excel} and from Graph {len_pdb_graph}")

   def get_common_atoms_values(self):     
      id_atoms_excel, id_atoms_graph = self.get_index_from_atoms()       
      common_values = list((set(id_atoms_excel).intersection(id_atoms_graph))) #Compute the intersection      
      if len(common_values) == 0:
         print("List of atoms from both PDB files have equals elements!!!!")
      else:
         a_in_b = list(set(id_atoms_excel) - set(id_atoms_graph))
         b_in_a = list(set(id_atoms_graph) - set(id_atoms_excel))
         if not self.show_results:
            print(f"CONECT elements in PDBExcel not present in PDBGraph: ({len(a_in_b)})")
            print(f"CONECT elements in PDBGraph not present in PDBExcel: ({len(b_in_a)})")
         else:         
            print(f"Elements in PDBExcel ({len(a_in_b)}) weren`t in PDBGraph")
            print(a_in_b)
            print(f"Elements in PDBGraph ({len(b_in_a)}) weren`t in PDBExcel")
            print(b_in_a)
  
   def get_common_conect_values(self):
      conect_excel = self.pdb_excel_concexion_data
      conect_graph = self.pdb_graph_concexion_data   
      common_values = list(set(conect_excel).intersection(set(conect_graph)))  
      #different_values = list(set(conect_excel).difference(set(conect_graph)))  
      if len(common_values) == 0:
         print("List of CONECT from both PDB files have equals elements!!!!")         
      else:
         a_in_b = list(set(conect_excel) - set(conect_graph))
         b_in_a = list(set(conect_graph) - set(conect_excel))
         if not self.show_results:            
            print(f"CONECT elements in PDBExcel not present in PDBGraph: ({len(a_in_b)})")
            print(f"CONECT elements in PDBGraph not present in PDBExcel: ({len(b_in_a)})")
         else:               
            print(f"CONECT elements in PDBExcel present in PDBGraph: {len(different_values)}")
            print(f"CONECT elements in PDBExcel not present in PDBGraph: ({len(a_in_b)})")
            print(a_in_b)
            print(f"CONECT elements in PDBGraph not present in PDBExcel: ({len(b_in_a)})")
            print(b_in_a)

   def get_equals_atoms_values(self):
      id_atoms_excel, id_atoms_graph = self.get_index_from_atoms()  
      atoms_excel = sorted(set(id_atoms_excel))
      atoms_graph = sorted(id_atoms_graph)   
      if atoms_excel == atoms_graph:
         print("The two ATOMs lists are equals!!!")
      else:
         print("The two ATOMs lists aren`t equals!!!")  

   def get_equals_conect_values(self):
      conect_excel = sorted(set(self.pdb_excel_concexion_data))
      conect_graph = sorted(set(self.pdb_graph_concexion_data))   
      if conect_excel == conect_graph:
         print("The two CONECTs lists are equals!!!")
      else:
         print("The two CONECTs lists aren`t equals!!!")  

   def help_dupes(self, list_):
      seen = set()
      dupes = [x for x in list_ if x in seen or seen.add(x)]  
      return dupes

   def check_for_repeated_atmos(self):
      id_atoms_excel, id_atoms_graph = self.get_index_from_atoms()       
      excel_dupes = self.help_dupes(id_atoms_excel)
      graph_dupes = self.help_dupes(id_atoms_graph)
      if not self.show_results:
         print(f"Number of ATOMS elements duplicates in PDBExcel {len(excel_dupes)}")
         print(f"Number of ATOMS elements duplicates in PDBGraph {len(graph_dupes)}")
      else:
         print(f"Number of elements duplicates in PDBExcel {len(excel_dupes)}")
         print(excel_dupes)
         print(f"Number of elements duplicates in PDBGraph {len(graph_dupes)}")
         print(graph_dupes)

   def get_duplicates(self, list_):
      duples = []
      counter_list = Counter(list_)
      if not any(count > 1 for count in counter_list.values()):
         return False, []
      else:
         for tup, count in counter_list.items():
            if count > 1:
               duples.append(tup)
         print(duples)      
         return True, []

   def check_for_repeated_conects(self):      
      excel_is_dup, excel_dup_val = self.get_duplicates(self.pdb_excel_concexion_data)
      graph_is_dup, graph_dup_val = self.get_duplicates(self.pdb_graph_concexion_data)
      if not excel_is_dup:
         print("PDB from Excel doesn`t have duplicated values")
      else:
         if not self.show_results:
            print(f"Number of CONECT elements duplicates in PDBExcel {len(excel_dup_val)}")
         else:
            print(f"Number of CONECT elements duplicates in PDBExcel {len(excel_dup_val)}")
            print(excel_dup_val)
      if not graph_is_dup:
         print("PDB from Graph doesn`t have duplicated values")
      else:
         if not self.show_results:
            print(f"Number of CONECT elements duplicates in PDBGraph {len(graph_dup_val)}")
         else:
            print(f"Number of CONECT elements duplicates in PDBGraph {len(graph_dup_val)}")
            print(graph_dup_val)     

   def algorithmATOMS(self):
      print("-------------------------------------------------------------------------------------")
      print("--------------------------------ATOMS ANALYSIS---------------------------------------")
      print("-------------------------------------------------------------------------------------")
      self.read_atoms_files() #Load data
      print("-------------------------------------------------------------------------------------")
      self.check_atoms_list_sizes() #Check sizes or number of atmos     
      print("-------------------------------------------------------------------------------------")    
      self.get_common_atoms_values() #Check common atoms in both PDB
      print("-------------------------------------------------------------------------------------")
      self.get_equals_atoms_values() #Check iquals values
      print("-------------------------------------------------------------------------------------")
      self.check_for_repeated_atmos() #Check repeated atmos in PDB   

   def algorithmCONECT(self):
      print("-------------------------------------------------------------------------------------")
      print("--------------------------------CONETC ANALYSIS--------------------------------------")
      print("-------------------------------------------------------------------------------------")
      self.read_conexion_files() #Load CONECT data      
      print("-------------------------------------------------------------------------------------")
      self.check_conect_list_sizes() #Check the length of both list 
      print("-------------------------------------------------------------------------------------") 
      self.get_common_conect_values() #Check if the are subsets
      print("-------------------------------------------------------------------------------------")
      self.get_equals_conect_values()
      print("-------------------------------------------------------------------------------------")
      self.check_for_repeated_conects()
   
def main(**kwargs):
   #Create the check class
   chk = CheckPDB(kwargs['url_excel'], kwargs['url_graph'], False)
   print("Url pdb_excel:", chk.excel_pdb_url)
   print("Url pdb_graph:", chk.graph_pdb_url)
   chk.algorithmATOMS()
   chk.algorithmCONECT()
   
if __name__ == "__main__":
   if len(sys.argv) < 3:
      print('Usage: {} output_filename'.format(sys.argv[0]), file=sys.stderr)
      sys.exit(1)
   main(url_excel=sys.argv[1], url_graph=sys.argv[2])
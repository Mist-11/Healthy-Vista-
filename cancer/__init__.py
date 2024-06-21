import pickle

with open("./model/BC_mapper.pkl", "rb") as file:
    x_mapper = pickle.load(file)
with open("./model/BC_labtrans.pkl", "rb") as file:
    labtrans = pickle.load(file)

in_features = 79
num_nodes = [32, 32]
out_features = labtrans.out_features
batch_norm = True
dropout = 0.1

new_columns = [
    'age_at_diagnosis', 'size', 'lymph_nodes_positive', 'stage', 'lymph_nodes_removed', 'NPI',
    'grade', 'grade.1', 'grade.2', 'histological', 'histological.1', 'histological.2', 'histological.3',
    'histological.4', 'histological.5', 'histological.6', 'histological.7', 'histological.8',
    'histological.9', 'histological.10', 'histological.11', 'ER_IHC_status', 'ER_IHC_status.1', 'ER_Expr',
    'ER_Expr.1', 'PR_Expz', 'PR_Expz.1', 'HER2_IHC_status', 'HER2_IHC_status.1', 'HER2_IHC_status.2',
    'HER2_IHC_status.3', 'HER2_SNP6_state', 'HER2_SNP6_state.1', 'HER2_SNP6_state.2', 'Her2_Expr',
    'Her2_Expr.1', 'Treatment', 'Treatment.1', 'Treatment.2', 'Treatment.3', 'Treatment.4', 'Treatment.5',
    'Treatment.6', 'Treatment.7', 'inf_men_status', 'inf_men_status.1', 'group', 'group.1', 'group.2',
    'group.3', 'group.4', 'cellularity', 'cellularity.1', 'cellularity.2', 'Pam50_Subtype', 'Pam50_Subtype.1',
    'Pam50_Subtype.2', 'Pam50_Subtype.3', 'Pam50_Subtype.4', 'Pam50_Subtype.5', 'int_clust_memb',
    'int_clust_memb.1', 'int_clust_memb.2', 'int_clust_memb.3', 'int_clust_memb.4', 'int_clust_memb.5',
    'int_clust_memb.6', 'int_clust_memb.7', 'int_clust_memb.8', 'int_clust_memb.9', 'site', 'site.1',
    'site.2', 'site.3', 'site.4', 'Genefu', 'Genefu.1', 'Genefu.2', 'Genefu.3'
]

record_columns = [
    'age_at_diagnosis', 'size', 'lymph_nodes_positive', 'stage', 'lymph_nodes_removed', 'NPI',
    'grade.0', 'grade.1', 'grade.2', 'histological.0', 'histological.1', 'histological.2', 'histological.3',
    'histological.4', 'histological.5', 'histological.6', 'histological.7', 'histological.8',
    'histological.9', 'histological.10', 'histological.11', 'ER_IHC_status.0', 'ER_IHC_status.1', 'ER_Expr.0',
    'ER_Expr.1', 'PR_Expz.0', 'PR_Expz.1', 'HER2_IHC_status.0', 'HER2_IHC_status.1', 'HER2_IHC_status.2',
    'HER2_IHC_status.3', 'HER2_SNP6_state.0', 'HER2_SNP6_state.1', 'HER2_SNP6_state.2', 'Her2_Expr.0',
    'Her2_Expr.1', 'Treatment.0', 'Treatment.1', 'Treatment.2', 'Treatment.3', 'Treatment.4', 'Treatment.5',
    'Treatment.6', 'Treatment.7', 'inf_men_status.0', 'inf_men_status.1', 'group.0', 'group.1', 'group.2',
    'group.3', 'group.4', 'cellularity.0', 'cellularity.1', 'cellularity.2', 'Pam50_Subtype.0', 'Pam50_Subtype.1',
    'Pam50_Subtype.2', 'Pam50_Subtype.3', 'Pam50_Subtype.4', 'Pam50_Subtype.5', 'int_clust_memb.0',
    'int_clust_memb.1', 'int_clust_memb.2', 'int_clust_memb.3', 'int_clust_memb.4', 'int_clust_memb.5',
    'int_clust_memb.6', 'int_clust_memb.7', 'int_clust_memb.8', 'int_clust_memb.9', 'site.0', 'site.1',
    'site.2', 'site.3', 'site.4', 'Genefu.0', 'Genefu.1', 'Genefu.2', 'Genefu.3'
]

HE_columns = ['Age', 'Sex', 'Steroid', 'Antivirals', 'Fatigue', 'Malaise', 'Anorexia', 'Liver Big', 'Liver Firm',
              'Spleen Palpable', 'Spiders', 'Ascites', 'Varices', 'Bilirubin', 'Alk Phosphate', 'Sgot', 'Albumin',
              'Protime', 'Histology']

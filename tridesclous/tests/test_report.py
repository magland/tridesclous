import shutil

from tridesclous.dataio import DataIO

from tridesclous.catalogueconstructor import CatalogueConstructor
from tridesclous import Peeler
from tridesclous.tests.testingtools import setup_catalogue
from tridesclous.tests.testingtools import ON_CI_CLOUD

from tridesclous.report import summary_catalogue_clusters, summary_noise, summary_after_peeler_clusters, generate_report


import matplotlib.pyplot as plt


def setup_module():
    setup_catalogue('test_report', dataset_name='striatum_rat')
    
    dataio = DataIO(dirname='test_report')
    initial_catalogue = dataio.load_catalogue(chan_grp=0)
    peeler = Peeler(dataio)
    peeler.change_params(catalogue=initial_catalogue,chunksize=1024)
    peeler.run(progressbar=False)

def teardown_module():
    shutil.rmtree('test_report')

def test_summary_catalogue_clusters():
    dataio = DataIO(dirname='test_report')

    #~ summary_catalogue_clusters(dataio, chan_grp=0)
    summary_catalogue_clusters(dataio, chan_grp=0, labels= [0])
    
def test_summary_noise():
    dataio = DataIO(dirname='test_report')
 
    
    summary_noise(dataio, chan_grp=0)
    
def test_summary_after_peeler_clusters():
    dataio = DataIO(dirname='test_report')
    summary_after_peeler_clusters(dataio, chan_grp=0,  labels= [0])
    
    summary_after_peeler_clusters(dataio, chan_grp=0,  labels= [0], neighborhood_radius=200)



def test_generate_report():
    dataio = DataIO(dirname='test_report')
    
    generate_report(dataio)
    

if __name__ == '__main__':
    
    #~ setup_module()
    
    #~ test_summary_catalogue_clusters()
    
    #~ test_summary_noise()
    
    #~ test_summary_after_peeler_clusters()
    
    #~ plt.show()
    
    test_generate_report()


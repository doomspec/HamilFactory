import wget

URL_FORM = "https://github.com/doomspec/HamilFactory/blob/main/hamils/{}/{}.op?raw=true"
Local_Hamil_Repo_Root = "./hamils"

def download_hamil(category, name):
    try:
        wget.download(URL_FORM.format(category, name), "{}/{}/{}.op".format(Local_Hamil_Repo_Root, category, name))
    except Exception as e:
        print("Failed to Retrieve Hamiltonian from remote.\nError msg: "+str(e))

if __name__ == '__main__':
    download_hamil("mol", "LiH_12_BK")

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

Driver = webdriver.Firefox()


def clicaElementoUrl(url):
    driver.find_element(By.XPATH, f'//a[contains(@href,"{url}")]').click()
    sleep(2)


def ScrollElemento(elemento):
    driver.execute_script("arguments[0].scrollIntoView();", elemento)
    sleep(2)


if __name__ == '__main__':
    consultaAluno = "/consulta_aluno/"
    consultaAlunoEspecifico = "/consulta_aluno/4kqdjSMdZGK6tMCKEbuU"

    driver = Driver
    driver.get("https://sistema-academia-web.herokuapp.com/login")


    # Login
    usuario = driver.find_element(By.NAME, "username")
    senha = driver.find_element(By.NAME, "password")

    usuario.send_keys("admin")
    senha.send_keys("123")
    driver.find_element(By.ID, "loginbutton").click()

    # Main Page
    sleep(2)
    clicaElementoUrl(consultaAluno)
    clicaElementoUrl(consultaAlunoEspecifico)

    # Botao PDF
    botaoPDF = driver.find_element(By.ID, "gerar_pdf")
    ScrollElemento(botaoPDF)
    botaoPDF.click()


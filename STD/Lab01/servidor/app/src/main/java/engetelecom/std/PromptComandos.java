package engetelecom.std;

import java.io.IOException;
import java.util.Hashtable;
import java.util.Scanner;

public class PromptComandos implements Runnable {

    private Hashtable<Integer, Cliente> clientes;

    public PromptComandos(Hashtable<Integer, Cliente> clientes) {
        this.clientes = clientes;
    }

    @Override
    public void run() {
        Scanner teclado = new Scanner(System.in);
        String comando = "";

        do{
            System.out.print("> ");
            final var finalComando = teclado.nextLine() + "\n";

            clientes.forEach((id, cliente) ->{
                try{
                    cliente.saida().writeBytes(finalComando);
                    if(!finalComando.equals("sair")){
                        System.out.println(cliente.entrada().readLine());
                    }
                } catch (IOException e){
                    System.err.println("Erro: " + e.getMessage());
                }
            });

        }while(!comando.equals("sair"));
        System.exit(0);
    }
}

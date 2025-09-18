package engtelecom.std;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;

public class AtenderCliente implements Runnable {

    private Socket cliente;

    public AtenderCliente(Socket cliente) {
        this.cliente = cliente;
    }

    @Override
    public void run() {
        if(cliente != null){
            try {
                System.out.println("Cliente - " + cliente.getInetAddress() +" conectado");

                // Estabelecimento dos fluxos de entrada e saída
                BufferedReader entrada = new BufferedReader(new InputStreamReader(cliente.getInputStream(), "UTF-8"));
                DataOutputStream saida = new DataOutputStream(cliente.getOutputStream());

                // Comunicação
                String recebido;
                do {
                    recebido = entrada.readLine();
                    if(!recebido.equals("sair")){
                        System.out.println(cliente.getInetAddress() + " > " + recebido);
                        saida.writeBytes("S > " + recebido.toUpperCase() + "\n");
                    } else {
                        System.out.println(cliente.getInetAddress() + " > Encerrou a conexão");
                    }
                } while (!recebido.equals("sair"));

            } catch (IOException e){
                System.err.println("Erro na thread: " + e.getMessage());
            }
        }
    }
}

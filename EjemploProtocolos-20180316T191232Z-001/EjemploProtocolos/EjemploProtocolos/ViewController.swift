//
//  ViewController.swift
//  EjemploProtocolos
//
//  Created by Christian Quicano on 10/26/17.
//  Copyright © 2017 Christian Quicano. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    fileprivate var contactos = [[String:Any]]()
//    fileprivate var contactos:[[String:String]] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        
//        inicializamos el array
        contactos.append([kTelefono:"965028331", kStatus:true])
        contactos.append([kTelefono:"982738495", kStatus:false])
        contactos.append([kTelefono:"473849686", kStatus:true])
        contactos.append([kTelefono:"948276495", kStatus:false])
        
    }

}

extension ViewController:UITableViewDelegate, UITableViewDataSource {
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return contactos.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "customCell", for: indexPath) as! CustomCell
        cell.configurarCelda(data: contactos[indexPath.row])
        cell.delegate = self
        return cell
        
    }
    
}

extension ViewController:CustomCellDelegate {
    func llamar(numero: String) {
        print(numero)
    }
    
    func cambiar(status: Bool) {
        print(status)
    }
    
}















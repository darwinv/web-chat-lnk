//
//  CustomCell.swift
//  EjemploProtocolos
//
//  Created by Christian Quicano on 10/26/17.
//  Copyright © 2017 Christian Quicano. All rights reserved.
//

import UIKit

protocol CustomCellDelegate:NSObjectProtocol {
    func llamar(numero:String)
    func cambiar(status:Bool)
}


class CustomCell: UITableViewCell {

    weak var delegate:CustomCellDelegate?
    
     @IBOutlet private weak var botonLlamar: UIButton!
     @IBOutlet private weak var activarUsuario: UISwitch!
    private var tel = ""
    private var status = false
    
    func configurarCelda(data:[String:Any]) {
        guard let telefono = data[kTelefono] as? String
            , let status = data[kStatus] as? Bool
            , telefono.characters.count > 0 else {
            return
        }
        tel = telefono
        self.status = status
        botonLlamar.setTitle(telefono, for: .normal)
        activarUsuario.isOn = status
    }
    
    
     @IBAction private func activar(_ sender: Any) {
        delegate?.cambiar(status: activarUsuario.isOn)
    }
    
     @IBAction private func llamar(_ sender: Any) {
        delegate?.llamar(numero: tel)
    }
}

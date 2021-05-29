import React from 'react';
import '../css/about.css';
import header from '../img/header_covid_project.png';

function AboutScreen() {
  return (
    <div>
      <div>
        <img src={header} className="sizing-header"/>
      </div>
      <div className="background-long">
        <div className="background">
          <h1>Tentang kami</h1>
        </div>
      </div>
      <p className="caption">
        Website ini merupakan sebuah mini project untuk mata kuliah Data Mining
        dari kelas LA06. <br/> 
        Dalam website ini menampilkan <b>penggambaran pasien covid-19
        yang meninggal</b> dengan menggunakan <b>clustering</b> dan juga melihat <b>outlier</b> dari data yang telah dipilih.</p>

      <div className="background-long">
        <div className="background">
          <h1>Kelompok</h1>
        </div>
      </div>
      <div className="caption">
        2001608755 - Fidela Sri Elvina <br/>
        2101667254 - Dewi Fortuna <br />
        2101668156 - Panji Krishna D <br />
        2101700586 - Afifa Ayu Widhiyanthi <br />
        2101707926 - Azzalia Chaeruni Putri<br />
      </div>
    </div>
  );
}

export default AboutScreen;
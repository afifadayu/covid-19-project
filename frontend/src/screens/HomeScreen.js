import React from 'react';
import BarChart from 'chart-race-react';
import header from '../img/header_covid_project.png';
import '../css/home.css';

function HomeScreen() {
  return (
    <div>
      <img src={header} className="sizing-header"/>
      <div className="lines">
        <div className="sq">
          <h1 className="title">Kasus COVID-19 Jakarta</h1>
        </div>
      </div>
      <div class="flexing">
        <div class="column-1 box">
          <div class="flexing">
            <div className="col boxing-case">
              <h4 className="case">Total Kasus</h4>
              <h2 className="count-black">425.212</h2>
            </div>
            <div className="col boxing-case">
              <h4 className="case">Total Sembuh</h4>
              <h2 className="count-green">407.493</h2>
            </div>
          </div>
          <div class="flexing">
            <div className="col boxing-case">
              <h4 className="case">Kasus Aktif</h4>
              <h2 className="count-black">10.480</h2>
            </div>
            <div className="col boxing-case">
              <h4 className="case">Total Meninggal</h4>
              <h2 className="count-red">7.239</h2>
            </div>
          </div>
          <div class="flexing">
            <div className="col boxing-case">
              <h4 className="case">Tingkat Kematian</h4>
              <h2 className="count-red">1.7%</h2>
            </div>
            <div className="col boxing-case">
              <h4 className="case">Tingkat Kesembuhan</h4>
              <h2 className="count-green">95.8%</h2>
            </div>
          </div>
        </div>
        <div class="column-2 box">
          <h1>What is Lorem Ipsum?</h1>
          <p>
            What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing
            and typesetting industry. Lorem Ipsum has been the industry's standard
            dummy text ever since the 1500s, when an unknown printer took a galley
            of type and scrambled it to make a type specimen book. It has survived
            not only five centuries, but also the leap into electronic
            typesetting, remaining essentially unchanged
        </p>
        </div>
      </div>
    </div>
  );
}

export default HomeScreen;
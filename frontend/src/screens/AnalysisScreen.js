import React, {useState} from 'react';
import DatePicker from 'react-datepicker';
import header from '../img/header_covid_project.png';
import 'react-datepicker/dist/react-datepicker.css';
import '../css/analysis.css';

function AnalysisScreen() {
  const [selectedDate, setSelectedDate] = useState(null);
  return (
    <div >
      <img src={header} className="sizing-header" />
      <div className="lines">
        <div className="sq">
          <h1 className="title">Analisis Data</h1>
        </div>
      </div>
      <div className="styling-content">
        <DatePicker selected={selectedDate}
          onChange={date => setSelectedDate(date)}
          dateFormat='dd/MM/yyyy'
          maxDate={new Date()}
          isClearable={false}
          />
        <div style={{paddingLeft:'20px'}}>
          <a href="" className="button">Analisis Data</a>
        </div>
      </div>
      <div class="flexing">
        <div class="my-column-1 box">
          <h1 style={{ textAlign: 'center' }}>CLUSTERING MAP OF DIED PATIENTS</h1>
          <p>
            What is Lorem Ipsum? Lorem Ipsum is simply dummy text of the printing
            and typesetting industry. Lorem Ipsum has been the industry's standard
            dummy text ever since the 1500s, when an unknown printer took a galley
            of type and scrambled it to make a type specimen book. It has survived
            not only five centuries, but also the leap into electronic
            typesetting, remaining essentially unchanged
        </p>
        </div>
        <div class="my-column-1 box">
          <h1 style={{textAlign: 'center'}}>OUTLIER</h1>
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

export default AnalysisScreen;
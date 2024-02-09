import {Fragment} from 'react';
import {connect} from 'react-redux';

import { Alert as AL } from 'flowbite-react';
import { HiInformationCircle } from 'react-icons/hi';

function Alert({ alert }) {

    const displayAlert = () => {
        if (alert !== null){
            return (
                // <div className={`rounded-md bg-${alert.alertType}-50 p-4`}>
                // <div className="flex">
                //     <div className="flex-shrink-0">
                //     <CheckCircleIcon className={`h-5 w-5 text-${alert.alertType}-400`} aria-hidden="true" />
                //     </div>
                //     <div className="ml-3">
                //     <p className={`text-sm font-medium text-${alert.alertType}-800`}>{alert.msg}</p>
                //     </div>
                // </div>
                // </div>

              <AL
                color={`${alert.alertType}`}
                icon={HiInformationCircle}
              >
                <span>
                  <p>
                    <span className="font-medium">
                      {alert.alertType} - &nbsp;
                    </span>
                    {alert.msg}
                  </p>
                </span>
              </AL>
            )
        } else {
            return(
                <Fragment></Fragment>
            )
        }
    }

    return (
        <Fragment>
            {displayAlert()}
        </Fragment>
    )
}

const mapStateToProps = state => ({
    alert: state.Alert.alert
})

export default connect(mapStateToProps)(Alert);
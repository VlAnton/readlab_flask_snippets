import React from 'react';
import b_ from 'b_';


const b = b_.with('create');

class CreateForm extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            isPublic: true,
            description: '',
            fileFields: ['input-0'],
            files: undefined
        }

        this.files = React.createRef()

        this.onChange = this.onChange.bind(this);
        this.onCheck = this.onCheck.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onChange(event) {
        const fieldName = event.target.name;
        const fieldValue = event.target.value;

        this.setState({[fieldName]: fieldValue})
    }

    onCheck(event) {
        switch (event.target.checked) {
            case false:
                this.setState({isPublic: false});
                break;

            default:
                this.setState({isPublic: true});
        }
    }

    async onSubmit(event) {
        event.preventDefault();
        var form = new FormData();
        let body = this.state;
        body['files'] = this.files;
        
        let filesCount = 0;

        Object.keys(body).forEach(fieldName => {
            if (fieldName === 'files') {
                form.append(fieldName, body[fieldName].current.files[0])
            }
            form.append(fieldName, body[fieldName]);
        });
        form.forEach(console.log)

        await fetch('http://0.0.0.0:5000/api/snippets', {
            method: 'post',
            // headers: {"Content-Type": "multipart/form-data"},
            body: form
        })
        .then(console.log)
        .catch(console.log);
    }

    render() {
        const { isPublic, description } = this.state;

        return (
            <div className={b()}>
                    <form onSubmit={this.onSubmit} method="post" encType="multipart/form-data">
                    <p>
                        Add file:
                        <input
                            type="file"
                            className="files"
                            name="files"
                            ref={this.files}
                            // onChange={this.onChange}
                            multiple />
                    </p>
                    <p>
                        Enter description: 
                        <input
                            type="text"
                            name="description"
                            value={description}
                            onChange={this.onChange} />
                    </p>
                    <p>
                        Do you want a private snippet?
                        <input
                            type="checkbox"
                            name="public"
                            value={isPublic}
                            onChange={this.onCheck} />
                    </p>
                    <p><input type="submit" /></p>
                </form>
            </div>
        )
    }
}


export default CreateForm